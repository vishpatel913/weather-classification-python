from mangum import Mangum
from fastapi import FastAPI

app = FastAPI(root_path="/prod")


@app.get("", include_in_schema=False)
@app.get("/health")
def read_root():
    return {"Welcome": "Welcome to the FastAPI on Lambda"}


handler = Mangum(app, lifespan="off", api_gateway_base_path="/prod")
