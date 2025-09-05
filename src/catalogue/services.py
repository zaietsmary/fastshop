from fastapi import Depends

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.repository import (
    ProductRepository, AdditionalProductsRepository, RecommendedProductsRepository,
    get_product_repository, get_additional_product_repository, get_recommended_product_repository,
)
from src.common.service import BaseService
from sqlalchemy import select

class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)

class AdditionalProductsService(BaseService[AdditionalProducts]):
    def __init__(self, repository: AdditionalProductsRepository):
        super().__init__(repository)

    async def list_for_product(self, primary_id: int):
        query = select(AdditionalProducts).where(AdditionalProducts.primary_id == primary_id)
        result = await self.repository.session.execute(query)
        return result.scalars().all()


def get_additional_product_service(repo: AdditionalProductsRepository = Depends(get_additional_product_repository)) -> AdditionalProductsService:
    return AdditionalProductsService(repository=repo)

class RecommendedProductsService(BaseService[RecommendedProducts]):
    def __init__(self, repository: RecommendedProductsRepository):
        super().__init__(repository)

    async def list_for_product(self, primary_id: int):
        query = select(RecommendedProducts).where(RecommendedProducts.primary_id == primary_id)
        result = await self.repository.session.execute(query)
        return result.scalars().all()

def get_recommended_product_service(repo: RecommendedProductsRepository = Depends(get_recommended_product_repository)) -> RecommendedProductsService:
    return RecommendedProductsService(repository=repo)