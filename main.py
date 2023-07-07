from fastapi.responses import RedirectResponse

from mangum import Mangum

from src import app
from src.models import FaunaModel


@app.on_event("startup")
async def startup():
    try:
        await FaunaModel.create_all()
    except Exception as e:
        print(e)

@app.get("/")
async def index():
    return RedirectResponse(url="/docs")

handler = Mangum(app)
