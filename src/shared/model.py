from typing import Optional
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    __tablename__ = "books"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, nullable=False, index=True)
    description: str = Field(default="",sa_column_kwargs={"name": "description"}  )


