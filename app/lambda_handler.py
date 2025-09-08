from mangum import Mangum
from main import app

# Mangum adapter for Lambda
handler = Mangum(app, lifespan="off")


def lambda_handler(event, context):
    return handler(event, context)
