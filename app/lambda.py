"""Lambda handler for FastAPI application."""

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(root_path="/dev")


@app.get("", include_in_schema=False)
@app.get("/health")
def read_root():
    """Root endpoint."""
    return {"Welcome": "Welcome to the FastAPI on Lambda"}


handler = Mangum(app, lifespan="off", api_gateway_base_path="/dev")
