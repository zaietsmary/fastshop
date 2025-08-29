from src.common.routes import BaseCrudPrefixes


class CatalogueRoutesPrefixes:
    product: str = '/product'


class ProductRoutesPrefixes(BaseCrudPrefixes):
    ...

class AddressRoutesPrefixes(BaseCrudPrefixes):
    ...