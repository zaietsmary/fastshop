from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Response,
    status,
)

from src.catalogue.models.database import Category
from src.catalogue.routes import (
    CategoryRoutesPrefixes, CatalogueRoutesPrefixes
)
from src.catalogue.services import get_category_service
from src.common.enums import TaskStatus
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.general.schemas.task_status import TaskStatusModel


router = APIRouter(prefix=CatalogueRoutesPrefixes.catalogue)

@router.get(
    CategoryRoutesPrefixes.search,
    status_code=status.HTTP_200_OK,
)
async def search(
    keyword: str,
    service: Annotated[get_category_service, Depends()],
):
    """
    Search categories in Elasticsearch by keyword.

    Returns:
        List of categories matching the search.
    """
    response = await service.search(keyword=keyword)

    return response

@router.post(
    CategoryRoutesPrefixes.update_index,
    status_code=status.HTTP_200_OK,
)
async def update_elastic(
    background_tasks: BackgroundTasks,
    service: Annotated[get_category_service, Depends()],
):
    """
    Update categories index in Elasticsearch in background.

    Returns:
        Task status.
    """
    status_model = await TaskStatusModel(status=TaskStatus.IN_PROGRESS).save_to_redis()

    background_tasks.add_task(service.update_category_index, status_model.uuid)

    return await TaskStatusModel().get_from_redis(uuid=status_model.uuid)