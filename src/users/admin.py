from sqladmin import ModelView

from src.users.models.sqlalchemy import (
    User,
    UserAddress,
)

from .models.sqlalchemy import BasketLine, Basket, OrderLine, Order

ADMIN_CATEGORY = 'Accounts'


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.phone_number]
    column_searchable_list = [User.email, User.first_name, User.last_name]
    icon = 'fa-solid fa-user'
    category = ADMIN_CATEGORY


class UserAddressAdmin(ModelView, model=UserAddress):
    column_list = [UserAddress.user, UserAddress.title, UserAddress.street]
    column_searchable_list = [UserAddress.user, UserAddress.title, UserAddress.city, UserAddress.street]
    icon = 'fa-solid fa-address-book'
    category = ADMIN_CATEGORY

class BasketLineAdmin(ModelView, model=BasketLine):
    icon = "fa-solid fa-icons"
    column_list = [BasketLine.quantity, BasketLine.price]
    column_searchable_list = [BasketLine.price]
    category = ADMIN_CATEGORY

class BasketAdmin(ModelView, model=Basket):
    icon = "fa-solid fa-basket-shopping"
    column_list = [Basket.status, Basket.price]
    column_searchable_list = [Basket.status]
    category = ADMIN_CATEGORY

class OrderLineAdmin(ModelView, model=OrderLine):
    icon = "fa-solid fa-question"
    column_list = [OrderLine.quantity, OrderLine.price]
    column_searchable_list = [OrderLine.price]
    category = ADMIN_CATEGORY

class OrderAdmin(ModelView, model=Order):
    icon = "fa-solid fa-truck"
    column_list = [Order.created_at,Order.number, Order.status, Order.shipping_method, Order.additional_info, Order.total_price, Order.shipping_price]
    column_searchable_list = [Order.number, Order.status, Order.shipping_method, Order.additional_info]
    category = ADMIN_CATEGORY

def register_hr_admin_views(admin):
    admin.add_view(UserAdmin)
    admin.add_view(UserAddressAdmin)

    admin.add_view(BasketLineAdmin)
    admin.add_view(BasketAdmin)
    admin.add_view(OrderLineAdmin)
    admin.add_view(OrderAdmin)
