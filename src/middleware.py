import asyncio

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from .handlers import app as api
from .openai import *
from .pinecone import *
from .tools.sitemap import SiteMapTool
from .typedefs import *


def bootstrap():
    app = FastAPI()

    pinecone = PineConeClient()
    openai = OpenAIClient()
    tool = SiteMapTool()

    @app.middleware("http")
    async def auth_middleware(request: Request, call_next: Callable) -> Response:
        token = request.headers.get("Authorization", None)
        request.state.token = token
        response = await call_next(request)
        return response

    @app.post("/api/chatbot")
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
        pages = await tool.run(namespace)
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

    @app.get("/api/chatbot/ingest")
    async def ingest(namespace: str):
        vectors = await get_embeddings(namespace)
        return await asyncio.gather(
            *[pinecone.upsert(namespace, vector) for vector in vectors]
        )

    app.include_router(api, prefix="/api")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
