from fastapi import Depends

from src.catalogue.models.pydantic import ProductModel, CategoryModel
from src.catalogue.repository import (
    ProductRepository,CategoryRepository,
    get_product_repository, get_category_repository
)
from src.common.service import BaseService


class ProductService(BaseService[ProductModel]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)

class CategoryService(BaseService[CategoryModel]):
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository)


def get_category_service(repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(repository=repo)
