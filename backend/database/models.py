from datetime import datetime
from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    description: str
    date: datetime | None = None
    completed: bool = False


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ItemUpdate(ItemBase):
    description: str | None = None
    date: datetime | None = None
    completed: bool | None = False
