from src.common.routes import BaseCrudPrefixes


class CatalogueRoutesPrefixes:
    product: str = '/product'
    category: str = '/category'

class ProductRoutesPrefixes(BaseCrudPrefixes):
    ...

class CategoryRoutesPrefixes(BaseCrudPrefixes):
    ...