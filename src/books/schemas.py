
from pydantic import BaseModel, Field


class CreateBookDto(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=1000)

class BookDto(BaseModel):
    id: int
    title: str
    description: str

    model_config = {"from_attributes": True}