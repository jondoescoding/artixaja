from enum import Enum

class OrderStatus(Enum):
    ORDER_PLACED = "Order Placed" 
    PROCESSING = "Processing"
    PACKAGED = "Packaged"
    DELIVERED = "Delivered"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"

class PaymentStatus(Enum):
    NOT_PAID = "Not Paid"
    PAID = "Paid"