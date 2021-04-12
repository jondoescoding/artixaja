from enum import Enum
#Enum Class orderStatus
class OrderStatus(Enum):
    ORDER_PLACED = "Order Placed" 
    PROCESSING = "Processing"
    PACKAGED = "Packaged"
    DELIVERED = "Delivered"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"

#Enum Class Payment Status
class PaymentStatus(Enum):
    NOT_PAID = "Not Paid"
    PAID = "Paid"