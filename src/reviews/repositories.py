from src.common.repository.beanie import BaseMongoRepository
from src.reviews.models.mongo import ProductReview, ProductAnalytics


class ProductReviewRepository(BaseMongoRepository[ProductReview]):
    __model__ = ProductReview

class ProductAnalyticsRepository(BaseMongoRepository[ProductAnalytics]):
    __model__ = ProductAnalytics