from typing import Optional

from fastapi import Depends

from src.authentication.security import verify_password
from src.common.service import BaseService
from src.users.models.pydantic import (
    UserModel, UserAddressDetailResponse, UserAddressListResponse
)
from src.users.models.sqlalchemy import UserAddress
from src.users.repository import (
    UserRepository, UserAddressRepository,
    get_user_repository, get_address_repository
)


class UserService(BaseService[UserModel]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def get_by_email(self, email: str):
        return await self.repository.get_by_email(email=email)

    async def authenticate(self, email: str, password: str) -> Optional[UserModel]:
        user = await self.get_by_email(email=email)

        if user is None or not verify_password(plain_password=password, hashed_password=user.hashed_password):
            return None
        else:
            return user


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repo)

class UserAddressService(BaseService[UserAddress]):
    def __init__(self, repository: UserAddressRepository):
        super().__init__(repository)

    async def get_by_user_list(self, user_id: int):
        return await self.repository.get_by_user(user_id=user_id)

    async def get_detail_for_user(self, address_id: int, user_id: int):
        address = await self.repository.get_detail(address_id=address_id)
        if address.user_id != user_id:
            raise PermissionError("Forbidden")
        return UserAddressDetailResponse.model_validate(address)

def get_address_service(repo: UserAddressRepository = Depends(get_address_repository)) -> UserAddressService:
    return UserAddressService(repository=repo)