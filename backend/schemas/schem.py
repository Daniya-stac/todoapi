from pydantic import BaseModel, Field
from datetime import datetime


class ItemsBase(BaseModel):
    description: str = Field(max_length=30)
    date: datetime | None = None
    completed: bool = False


class ItemsUpdate(BaseModel):
    description: str = Field(default=None, max_length=30)
    date: datetime | None = None
    completed: bool | None = False


class ItemsCreate(ItemsBase):
    pass


class ItemsResponse(ItemsBase):
    id: int
