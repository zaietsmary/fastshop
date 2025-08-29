from typing import Union, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Union[int, None] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str


class UserWithPassword(UserModel):
    hashed_password: str

class UserAddressListResponse(BaseModel):
    id: int
    title: str

class UserAddressDetailResponse(BaseModel):
    id: int
    title: Optional[str]
    city: str
    street: str
    house: str
    apartment: Optional[str]
    post_code: Optional[str]
    floor: Optional[str]
    additional_info: Optional[str]