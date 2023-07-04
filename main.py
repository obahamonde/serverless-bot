from mangum import Mangum

from src import app

handler = Mangum(app)
