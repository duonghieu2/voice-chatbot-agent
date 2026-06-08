from pydantic import BaseModel
from typing import List, Optional

class FoodOrderItem(BaseModel):
    name: str
    qty: int
    price: float

class FoodOrderResponse(BaseModel):
    id: str
    user_id: str
    restaurant_name: str
    status: str
    items: List[FoodOrderItem]
    subtotal: float
    delivery_fee: float
    discount: float
    total: float
    payment_method: str
    payment_status: str
    eta: str
    items_missing: List[str]
    created_at: str

class FoodOrderStatusResponse(BaseModel):
    order_id: str
    status: str
    restaurant_name: str
    eta: str
    items_missing: List[str]
    total: float
    payment_status: str
