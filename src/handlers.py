from fastapi import APIRouter

from .tools.sitemap import SiteMapTool

tool = SiteMapTool()
app = APIRouter()


@app.get("/sitemap")
async def get_sitemap(url: str):
    return await tool.run(url)
