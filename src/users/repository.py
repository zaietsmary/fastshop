from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository
from src.users.models.pydantic import (
    UserModel,
    UserWithPassword, UserAddressDetailResponse, UserAddressListResponse
)
from src.users.models.sqlalchemy import User, UserAddress
from src.common.exceptions.base import ObjectDoesNotExistException

class UserRepository(BaseSQLAlchemyRepository[User, UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, pydantic_model=UserModel, session=session)

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[UserWithPassword]:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None

        return UserWithPassword.model_validate(user)


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)

class UserAddressRepository(BaseSQLAlchemyRepository[UserAddress, UserAddressDetailResponse]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserAddress, pydantic_model=UserAddressDetailResponse, session=session)

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def get_by_user(self, user_id : int) -> list[UserAddressListResponse]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        addresses = result.scalars().all()
        return [UserAddressListResponse.model_validate(a) for a in addresses]

    async def get_detail(self, address_id: int) -> UserAddressDetailResponse:
        stmt = select(self.model).where(self.model.id == address_id)
        result = await self.session.execute(stmt)
        address = result.scalar_one_or_none()
        if not address:
            raise ObjectDoesNotExistException(f"Address with id {address_id} not found")
        return UserAddressDetailResponse.model_validate(address)

def get_address_repository(session: AsyncSession = Depends(get_session)) -> UserAddressRepository:
    return UserAddressRepository(session=session)