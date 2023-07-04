import asyncio
import json
import re
from typing import List

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field



class Page(BaseModel):
    title: str = Field(..., description="Title of the page")
    url: str = Field(..., description="Url of the page")
    content: str = Field(..., description="Content of the page")

    def __init__(self, **data):
        super().__init__(**data)
        self.content = self.clean_text(self.content)

    def clean_text(self, text: str) -> str:
        # Strip out newline, tab, and carriage return characters
        text = text.replace("\n", " ").replace("\r", "").replace("\t", " ")

        # Replace encoded Spanish punctuation with actual characters
        text = (
            text.replace("&aacute;", "á")
            .replace("&eacute;", "é")
            .replace("&iacute;", "í")
            .replace("&oacute;", "ó")
            .replace("&uacute;", "ú")
        )
        text = (
            text.replace("&Aacute;", "Á")
            .replace("&Eacute;", "É")
            .replace("&Iacute;", "Í")
            .replace("&Oacute;", "Ó")
            .replace("&Uacute;", "Ú")
        )
        text = (
            text.replace("&ntilde;", "ñ")
            .replace("&Ntilde;", "Ñ")
            .replace("&iexcl;", "¡")
            .replace("&iquest;", "¿")
        )

        # Optionally, remove any additional unwanted characters (e.g., HTML tags)
        text = re.sub("<.*?>", "", text)  # Remove HTML tags
        text = re.sub("\s+", " ", text)  # Replace multiple spaces with a single space
        return text.strip()


class SiteMapTool:
    def __init__(self, max_connections: int = 1000):
        self.urls: List[str] = []
        self.pages: List[Page] = []
        self.semaphore = asyncio.Semaphore(max_connections)

    async def fetch_loc(self, url: str):
        async with self.semaphore, ClientSession() as session:
            async with session.get(url) as response:
                try:
                    assert response.status == 200
                    html = (await response.text()).strip()
                    soup = BeautifulSoup(html, "lxml")
                except:
                    return self.urls
                # Check for nested sitemap (sitemaps that point to other sitemaps)
                sitemaps = soup.find_all("sitemap")
                if sitemaps:
                    for sitemap in sitemaps:
                        loc = sitemap.find("loc").text
                        await self.fetch_loc(loc)
                else:
                    # If no nested sitemaps are found, fetch the 'loc' tags
                    locs = soup.find_all("loc")
                    for loc in locs:
                        text = loc.text
                        self.urls.append(text)
                return self.urls

    async def fetch_sitemap(self, url: str):
        sitemap_url = url if url.endswith("sitemap.xml") else f"{url}/sitemap.xml"
        return await self.fetch_loc(sitemap_url)

    async def fetch_page(self, url: str) -> Page:
        async with self.semaphore, ClientSession() as session:
            async with session.get(url) as response:
                try:
                    assert response.status == 200
                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")
                    if soup.title is None:
                        page = Page(title=url, url=url, content="")
                    else:
                        page = Page(title=soup.title.text, url=url, content=soup.text)
                except:
                    page = Page(title=url, url=url, content="")
                finally:
                    self.pages.append(page)
                    await asyncio.sleep(0.1)
                    progress = len(self.pages) / len(self.urls)
                    print(f"{progress:.2%} complete")
                    return page

    async def run(self, url: str):
        urls = await self.fetch_sitemap(url)
        for url in urls:
            try:
                await self.fetch_page(url)
            except:
                await asyncio.sleep(0.1)
                progress = len(self.pages) / len(self.urls)
                print(f"{progress:.2%} complete")
                continue
            finally:
                await asyncio.sleep(0.1)
                progress = len(self.pages) / len(self.urls)
                print(f"{progress:.2%} complete")

        return self.pages
