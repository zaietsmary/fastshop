from src.common.routes import BaseCrudPrefixes


class UserManagementRoutesPrefixes:
    user: str = '/user'


class UserRoutesPrefixes(BaseCrudPrefixes):
    root = "/addresses"
    detail = "/addresses/{address_id}"
