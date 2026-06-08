from pydantic import BaseModel
from typing import Optional

class SupportTicketCreate(BaseModel):
    user_id: str
    category: str  # e.g., 'ride_issue', 'food_issue', 'payment_issue'
    description: str

class SupportTicketResponse(BaseModel):
    id: str
    user_id: str
    category: str
    description: str
    status: str
    created_at: str
