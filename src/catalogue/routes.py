from src.common.routes import BaseCrudPrefixes


class CatalogueRoutesPrefixes:
    product: str = '/product'
    catalogue: str = '/catalogue'

class ProductRoutesPrefixes(BaseCrudPrefixes):
    search: str = '/search'
    update_index: str = '/update-index'

class CategoryRoutesPrefixes(BaseCrudPrefixes):
    search: str = '/search'
    update_index = '/update-index'