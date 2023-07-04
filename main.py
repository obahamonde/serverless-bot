import asyncio
from dataclasses import dataclass, field
from typing import *

from aiohttp import ClientSession
from fastapi import FastAPI
from mangum import Mangum
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy
from pydantic import BaseModel, Field

Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
Headers = Union[CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy, Dict[str, str]]
Json = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

@dataclass
class ApiClient:
    base_url: str   
    headers: Headers = field(default_factory=dict)
    
    async def fetch(self, method: Method, url: str, headers: Headers = {}, json: Json = None):
        async with ClientSession(base_url=self.base_url, headers=self.headers) as session:
            async with session.request(method, url, headers=headers, json=json) as resp:
                return await resp.json()
            
    async def get(self, url: str, headers: Headers = {}):
        return await self.request("GET", url, headers=headers)
    
    async def post(self, url: str, headers: Headers = {}, json: Json = None):
        return await self.request("POST", url, headers=headers, json=json)
    
    async def put(self, url: str, headers: Headers = {}, json: Json = None):
        return await self.request("PUT", url, headers=headers, json=json)
    
    async def delete(self, url: str, headers: Headers = {}, json: Json = None):
        return await self.request("DELETE", url, headers=headers, json=json)
    
    async def patch(self, url: str, headers: Headers = {}, json: Json = None):
        return await self.request("PATCH", url, headers=headers, json=json)
    
    async def text(self, url: str, method: Method="GET", headers: Headers = {}, json: Json = None):
        async with ClientSession(base_url=self.base_url, headers=self.headers) as session:
            async with session.request(method, url, headers=headers, json=json) as resp:
                return await resp.text()
            
    async def stream(self, url: str, method: Method="GET", headers: Headers = {}, json: Json = None):
        async with ClientSession(base_url=self.base_url, headers=self.headers) as session:
            async with session.request(method, url, headers=headers, json=json) as resp:
                async for data in resp.content.iter_chunked(1024):
                    yield data.decode("utf-8")
                
    async def blob(self, url: str, method: Method="GET", headers: Headers = {}, json: Json = None):
        async with ClientSession(base_url=self.base_url) as session:
            async with session.request(method, url, headers=headers, json=json) as resp:
                return await resp.read()
            
    


app = FastAPI()

def url_get(i:int)->str:
    return f"https://jsonplaceholder.typicode.com/todos/{i}"

async def get(url:str):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

@app.get("/")
async def read_root():
   
    return await asyncio.gather(*[get(url_get(i)) for i in range(1, 100)])

handler = Mangum(app)
