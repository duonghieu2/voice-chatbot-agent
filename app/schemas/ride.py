from pydantic import BaseModel
from typing import Optional

class RideBase(BaseModel):
    user_id: str
    pickup_address: str
    dropoff_address: str

class RideCreate(RideBase):
    pass

class RideResponse(BaseModel):
    id: str
    user_id: str
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    vehicle_plate: Optional[str] = None
    vehicle_type: str
    status: str
    pickup_address: str
    dropoff_address: str
    price: float
    payment_method: str
    payment_status: str
    eta: str
    created_at: str

class RideStatusResponse(BaseModel):
    ride_id: str
    status: str
    driver_name: Optional[str] = None
    vehicle_plate: Optional[str] = None
    eta: str
    payment_status: str

class RideCancelRequest(BaseModel):
    ride_id: str
    reason: Optional[str] = None

class RideCancelResponse(BaseModel):
    ride_id: str
    status: str
    message: str
