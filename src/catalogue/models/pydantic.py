from typing import Optional

from pydantic import (
    BaseModel,
    constr,
)


class ProductModel(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    short_description: Optional[constr(max_length=20)]
    is_active: bool

    class Config:
        from_attributes = True

class CategoryModel(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    image: Optional[str]
    is_active: bool
    parent_id: Optional[int]

    class Config:
        from_attributes = True