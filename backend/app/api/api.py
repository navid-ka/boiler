from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.db.dynamodb import get_dynamodb
from botocore.exceptions import ClientError
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
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
            logger.info("DynamoDB table 'Items' created successfully.")
        else:
            logger.info("DynamoDB table 'Items' already exists.")
    except ClientError as err:
        logger.error(
            "Couldn't create table 'Items'. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise

    yield

    logger.info("Application shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(v1_router, prefix="/api/v1")
