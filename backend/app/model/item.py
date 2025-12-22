from pydantic import BaseModel

class ItemCreate(BaseModel):
    title: str
    description: str

class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None