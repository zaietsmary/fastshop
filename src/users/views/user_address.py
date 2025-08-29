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

from src.catalogue.models.pydantic import ProductModel
from src.users.models.sqlalchemy import UserAddress
from src.users.models.pydantic import UserAddressListResponse, UserAddressDetailResponse
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes, AddressRoutesPrefixes,
)
from src.catalogue.services import get_product_service
from src.users.services import get_address_service, UserAddressService
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.authentication.utils import get_current_user

router = APIRouter(prefix=CatalogueRoutesPrefixes.product)


@router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[ProductModel],
)
async def product_list(product_service: Annotated[get_product_service, Depends()]) -> list[ProductModel]:
    """
    Get list of products.

    Returns:
        Response with list of products.
    """
    return await product_service.list()


@router.get(
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






@router.get(
    AddressRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[UserAddressListResponse],
)
async def address_list(
    address_service: Annotated[UserAddressService, Depends(get_address_service)],
    current_user = Depends(get_current_user),
) -> list[UserAddressListResponse]:
    """
    Get list of addresses for the current user.
    """
    addresses = await address_service.get_by_user_list(user_id=current_user.id)
    return addresses


@router.get(
    AddressRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': UserAddress},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[UserAddressDetailResponse, ErrorResponse],
)
async def address_detail(
    address_id: int,
    response: Response,
    address_service: Annotated[UserAddressService, Depends(get_address_service)],
    current_user = Depends(get_current_user),
) -> Union[UserAddressDetailResponse, ErrorResponse]:
    """
    Retrieve address details for the current user.
    """
    try:
        address = await address_service.get_detail_for_user(
            address_id=address_id,
            user_id=current_user.id
        )
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)
    except PermissionError:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(message="Forbidden")

    return address