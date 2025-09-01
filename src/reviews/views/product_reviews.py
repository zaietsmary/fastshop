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

from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.reviews.models.mongo import (
    BaseProductReview,
    ProductReview, ProductAnalytics,
    Reply,
)
from src.reviews.routes import (
    ProductReviewRoutesPrefixes,
    ReviewsRoutesPrefixes, ProductAnalyticsPrefixes
)
from src.reviews.services import ProductReviewService, ProductAnalyticsService


router = APIRouter(prefix=ReviewsRoutesPrefixes.product_reviews)

@router.get(
    ProductReviewRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[BaseProductReview],
)
async def product_review_list(
    product_review_service: Annotated[ProductReviewService, Depends()],
) -> list[BaseProductReview]:
    """
    Get list of product reviews.
    Returns:
        Response with list of product reviews.
    """
    return await product_review_service.list()


@router.get(
    ProductReviewRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': ProductReview},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[ProductReview, ErrorResponse],
)
async def product_review_detail(
    response: Response,
    pk: str,
    service: Annotated[ProductReviewService, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve product review.
    Returns:
        Response with product review details.
    """
    try:
        response = await service.detail_with_replies(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@router.post(
    ProductReviewRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=ProductReview,
)
async def add_product_review(review: BaseProductReview, service: ProductReviewService = Depends()):
    """
    Add product review.
    Returns:
        Response with product review details.
    """
    new_instance = await service.create(instance_data=review)
    return new_instance


@router.post(
    ProductReviewRoutesPrefixes.add_reply,
    responses={
        status.HTTP_200_OK: {'model': ProductReview},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[BaseProductReview, ErrorResponse],
)
async def add_reply_to_review(
    response: Response,
    pk: str,
    reply: Reply,
    service: ProductReviewService = Depends(),
):
    """
    Add reply to product review.
    Returns:
        Response with product review details.
    """
    try:
        response = await service.add_reply(pk=pk, reply=reply)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response




@router.post(
    ProductAnalyticsPrefixes.product_detail,
    responses={
        status.HTTP_200_OK: {'model': ProductAnalytics},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[ProductAnalytics, ErrorResponse],
)
async def add_record(
    response: Response,
    pk: int,
    service: ProductAnalyticsService = Depends(),
):

    try:
        response = await service.visit_information(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response