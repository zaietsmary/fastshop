from enum import Enum

class BasketStatusEnum(str, Enum):
    Open = "Open"
    Closed = "Closed"
    Cancelled = "Cancelled"

class OrderStatusEnum(str, Enum):
    Open = "Open"
    Paid = "Paid"
    Sent = "Sent"
    Received = "Received"
    Cancelled = "Cancelled"
    Returned = "Returned"