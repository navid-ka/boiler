from fastapi import APIRouter, Depends
from app.db.dynamodb import get_items_table
from app.model.item import ItemCreate
from app.model.item import ItemUpdate
from uuid import uuid4

import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/")
def create_item(item: ItemCreate, table=Depends(get_items_table)):
    item_id = str(uuid4())

    try:
        table.put_item(
            Item={
                "id": item_id,
                "title": item.title,
                "description": item.description,
            }
        )
        logger.info("Created item %s", item_id)

    except ClientError as err:
        logger.error(
            "Couldn't create item %s. %s: %s",
            item_id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise

    return {"id": item_id}


@router.delete("/{id}")
def delete_item(id: str, table=Depends(get_items_table)):
    try:
        table.delete_item(Key={"id": id})
        logger.info("Deleted item %s", id)

    except ClientError as err:
        logger.error(
            "Couldn't delete item %s. %s: %s",
            id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise

#https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/dynamodb/GettingStarted/update_and_query.py
@router.patch("/{id}")
def update_item(
    id: str,
    item: ItemUpdate,
    table=Depends(get_items_table),
):
    try:
        response = table.update_item(
            Key={"id": id},
            UpdateExpression="SET #t = :t, #d = :d",
            ConditionExpression="attribute_exists(id)",
            ExpressionAttributeNames={
                "#t": "title",
                "#d": "description",
            },
            ExpressionAttributeValues={
                ":t": item.title,
                ":d": item.description,
            },
            ReturnValues="ALL_NEW",
        )

    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            logger.warning("Item %s does not exist — update skipped", id)
        else:
            logger.error(
                "Couldn't update item %s. %s: %s",
                id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
        raise

    else:
        logger.info("Updated item %s", id)
        return response["Attributes"]


@router.get("/")
def get_items(table=Depends(get_items_table)):
    try:
        response = table.scan()
        items = response.get("Items", [])
        logger.info("Fetched %d items", len(items))
        return items

    except ClientError as err:
        logger.error(
            "Couldn't fetch items. %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
