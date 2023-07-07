import asyncio

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from geocoder import ip

from .handlers import *


def bootstrap():
    app = FastAPI()

    @app.middleware("http")
    async def auth_middleware(request: Request, call_next: Callable) -> Response:
        token = request.headers.get("Authorization", None)
        request.state.token = token
        response = await call_next(request)
        return response
    
    @app.middleware("http")
    async def lead_gen_middleware(request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        lead_id = request.cookies.get("lead_id", None)
        client = request.client
        if client is None:
            raise HTTPException(400, "No client found")
        if client.host is None:
            raise HTTPException(400, "No host found")
        geo_data = ip(client.host).json["raw"]
        now = datetime.now().timestamp()
        if lead_id is None:
            lead_id = uuid4().hex
            response.set_cookie("lead_id", lead_id)
        ip_addr = client.host
        if not ip_addr:
            ip_addr = "0.0.0.0"
        lead = Lead(ipaddr=ip_addr, lead_id=lead_id, geo_data=geo_data)
        if isinstance(lead.visits, list):
            lead.visits.append(now)
        else:
            lead.visits = [now]
        await lead.save()
        return response
    

    app.include_router(api, prefix="/api")
    app.mount("/", StaticFiles(directory="static",html=True), name="static")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
