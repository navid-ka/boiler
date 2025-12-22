from fastapi import APIRouter, Depends
from uuid import uuid4
from app.db.dynamodb import get_items_table

router = APIRouter()

@router.post("/")
def create_item(table=Depends(get_items_table)):
    item_id = str(uuid4())
    table.put_item(Item={"id": item_id})
    return {"id": item_id}

@router.get("/")
def get_items(table=Depends(get_items_table)):
    response = table.scan()
    return response.get("Items", [])
