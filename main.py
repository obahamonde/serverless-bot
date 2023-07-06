from mangum import Mangum

from src import app
from src.models import FaunaModel


@app.on_event("startup")
async def startup():
    await FaunaModel.create_all()


handler = Mangum(app)
