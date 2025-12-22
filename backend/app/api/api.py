from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.db.dynamodb import get_dynamodb
from botocore.exceptions import ClientError
import logging

app = FastAPI()

app.include_router(v1_router, prefix="/api/v1")

@app.get("/api/v1")
async def root():
    return {"message": "Hello, World!"}

@app.on_event("startup")
def create_tables():
    try:
        dynamodb = get_dynamodb()
        existing = dynamodb.meta.client.list_tables()["TableNames"]

        if "Items" not in existing:
            table = dynamodb.create_table(
                TableName="Items",
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            table.wait_until_exists()
    except ClientError as err:
        logger.error(
            "Couldn't create table %s. Here's why: %s: %s",
            table,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
            )
        raise