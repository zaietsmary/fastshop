from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum,
    DECIMAL,
    Sequence,
)
from sqlalchemy.orm import relationship

from src.general.databases.postgres import Base
from ..enums.status import BasketStatusEnum, OrderStatusEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_temporary = Column(Boolean, default=False)

    addresses = relationship('UserAddress', back_populates='user')
    orders = relationship('Order', back_populates='user')


class UserAddress(Base):
    __tablename__ = 'user_addresses'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=True)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    apartment = Column(String, nullable=True)
    post_code = Column(String, nullable=True)
    floor = Column(String, nullable=True)
    additional_info = Column(String, nullable=True)

    user = relationship('User', back_populates='addresses')
    orders = relationship('Order', back_populates='user_address')


class BasketLine(Base):
    __tablename__ = 'basket_lines'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    basket_id = Column(Integer, ForeignKey('baskets.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))

    basket = relationship("Basket", back_populates="basketlines")
    product = relationship("Product", back_populates="basketlines")

class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    price = Column(DECIMAL(10, 2))
    status = Column(Enum(BasketStatusEnum), nullable=False, default=BasketStatusEnum.Open)

    basketlines = relationship("BasketLine", back_populates="basket")
    orders = relationship("Order", back_populates="basket")

class OrderLine(Base):
    __tablename__ = 'order_lines'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))

    order = relationship("Order", back_populates="orderlines")
    product = relationship("Product", back_populates="orderlines")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, Sequence('order_number_seq', start=10000), unique=True)
    basket_id = Column(Integer, ForeignKey('baskets.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('user_addresses.id'), nullable=False)
    total_price = Column(DECIMAL(10, 2))
    shipping_price = Column(DECIMAL(10, 2))
    shipping_method = Column(String, nullable=True)
    status = Column(Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.Open)
    additional_info = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    basket = relationship("Basket", back_populates="orders")
    user = relationship("User", back_populates="orders")
    user_address = relationship("UserAddress", back_populates="orders")
    orderlines = relationship("OrderLine", back_populates="order")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    basketlines = relationship("BasketLine", back_populates="product")
    orderlines = relationship("OrderLine", back_populates="product")

