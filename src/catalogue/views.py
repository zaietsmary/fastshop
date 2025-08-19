from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from src.catalogue.models.pydantic import ProductModel, CategoryModel
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
    CategoryRoutesPrefixes,
)
from src.catalogue.services import (
    get_product_service, get_category_service
)
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse


product_router = APIRouter(prefix=CatalogueRoutesPrefixes.product)
category_router = APIRouter(prefix=CatalogueRoutesPrefixes.category)

@product_router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[ProductModel],
)
# async def product_list(product_service: Annotated[get_product_service, Depends()]) -> list[ProductModel]:
async def product_list(product_service=Depends(get_product_service)) -> list[ProductModel]:

    """
    Get list of products.

    Returns:
        Response with list of products.
    """
    return await product_service.list()


@product_router.get(
    ProductRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': ProductModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[ProductModel, ErrorResponse],
)
async def product_detail(
    response: Response,
    pk: int,
    service: Annotated[get_product_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve product.

    Returns:
        Response with product details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@category_router.get(
    CategoryRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryModel],
)

async def category_list(category_service=Depends(get_category_service)) -> list[CategoryModel]:

    """
    Get list of categories.

    Returns:
        Response with list of categories.
    """
    return await category_service.list()


@category_router.get(
    CategoryRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': CategoryModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[CategoryModel, ErrorResponse],
)
async def category_detail(
    response: Response,
    pk: int,
    service: Annotated[get_category_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve category.

    Returns:
        Response with category details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response