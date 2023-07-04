import asyncio

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from mangum import Mangum

from src.handlers import app as api
from src.openai import *
from src.pinecone import *
from src.tools.sitemap import SiteMapTool

app = FastAPI()

pinecone = PineConeClient()
openai = OpenAIClient()
tool = SiteMapTool()
    

@app.post("/")
async def main(request: OpenAIEmbeddingRequest):
    vector = (await openai.post_embeddings(request)).data[0].embedding
    ctx = await pinecone.get_context(
        namespace=request.namespace, vector=vector, text=request.input
    )
    await pinecone.upsert(
        PineconeVectorUpsert(
            namespace=request.namespace,
            vectors=[PineconeVector(values=vector)],
            metadata={"text": request.input},
        )
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
        PineconeVectorUpsert(
            namespace=request.namespace,
            vectors=[PineconeVector(values=[])],
            metadata={"text": text},
        )
    )
    return PlainTextResponse(text)


@app.get("/")
async def main_(namespace:str):
    pages = await tool.run(namespace)
    requests = [
        OpenAIEmbeddingRequest(input=page.content, namespace=namespace) for page in pages
    ]
    responses = await asyncio.gather(*[openai.post_embeddings(req) for req in requests])
    vectors = [res.data[0].embedding for res in responses]
    await asyncio.gather(
        *[
            pinecone.upsert(
                PineconeVectorUpsert(
                    namespace=namespace,
                    vectors=[PineconeVector(values=vector)],
                    metadata={"text": page.content, "url": page.url},
                )
            )
            for page, vector in zip(pages, vectors)
        ]
    )
    return pages



app.include_router(api, prefix="/api")


handler = Mangum(app)