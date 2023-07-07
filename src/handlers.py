import asyncio

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import PlainTextResponse, StreamingResponse

from .apis import *
from .tools import *

api = APIRouter()

@api.post("/chatbot")
async def main(request: OpenAIEmbeddingRequest):
    vector = (await openai.post_embeddings(request)).data[0].embedding
    ctx = await pinecone.get_context(
        namespace=request.namespace, vector=vector, text=request.input
    )
    req = OpenAIChatCompletionRequest(
        prompt=request.input,
        namespace=request.namespace,
        context=ctx,
        role="lead-generation-machine",
    )
    content = req.chain()
    gpt_request = OpenAIChatGptRequest().chain(content, request.input)
    response = await openai.text_completion(gpt_request)
    text = response.choices[0].message.content
    vector = (
        (
            await openai.post_embeddings(
                OpenAIEmbeddingRequest(input=text, namespace=request.namespace)
            )
        )
        .data[0]
        .embedding
    )
    await pinecone.upsert(
        request.namespace,
        PineconeVector(
            values=vector,
            metadata={"text": text},
        ),
    )
    return PlainTextResponse(text)

async def get_embeddings(namespace: str):
    pages = await sitemap_tool.run(namespace)
    requests = [
        OpenAIEmbeddingRequest(input=page.content, namespace=namespace)
        for page in pages
    ]
    responses: List[OpenAIEmbeddingResponse] = await asyncio.gather(
        *[openai.post_embeddings(request) for request in requests]
    )
    embeddings = [response.data[0].embedding for response in responses]
    vectors = [
        PineconeVector(values=vector, metadata={"text": page.content})
        for vector, page in zip(embeddings, pages)
    ]
    return vectors

async def ingest_data(namespace: str):
    vectors = await get_embeddings(namespace)
    data = await asyncio.gather(
        *[pinecone.upsert(namespace, vector) for vector in vectors]
    )
    return data

@app.get("/chatbot/ingest")
async def ingest(background_tasks: BackgroundTasks, namespace: str):
    background_tasks.add_task(ingest_data, namespace)
    return {"message": "Ingestion started in the background"}
  
@api.post("/audio")
async def audio(text:str):
    polly = Polly.from_text(text)
    return StreamingResponse(polly.get_audio(), media_type="application/octet-stream")