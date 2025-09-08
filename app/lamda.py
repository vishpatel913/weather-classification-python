from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome": "Welcome to the FastAPI on Lambda"}


handler = Mangum(app)
