from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.core.tools import TOOL_DEFINITIONS
from app.services.tool_service import tool_service
from app.database.mock_db import db
from app.schemas.ticket import SupportTicketCreate, SupportTicketResponse

router = APIRouter()

@router.get("/tools/definitions")
def get_definitions() -> Dict[str, List[Dict[str, Any]]]:
    """Trả về danh sách định nghĩa JSON Schema của 6 công cụ cốt lõi phục vụ Tool Calling."""
    return {"tools": TOOL_DEFINITIONS}

@router.get("/tools/ride-status/{ride_id}")
def check_ride_status(ride_id: str) -> Dict[str, Any]:
    """API Mock cho check_ride_status tool."""
    clean_id = ride_id.upper()
    ride = tool_service.get_ride_status(clean_id)
    if not ride:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy chuyến xe {clean_id}")
    return ride

@router.get("/tools/order-status/{order_id}")
def check_order_status(order_id: str) -> Dict[str, Any]:
    """API Mock cho check_order_status tool."""
    clean_id = order_id.upper()
    order = tool_service.get_food_order_status(clean_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy đơn hàng {clean_id}")
    return order

@router.get("/tools/billing-fees/{target_id}")
def verify_billing_fees(target_id: str) -> Dict[str, Any]:
    """API Mock cho verify_billing_fees tool."""
    clean_id = target_id.upper()
    payment = tool_service.check_payment_status(clean_id)
    if not payment:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy thông tin cước phí/giao dịch của {clean_id}")
    return payment

@router.get("/tools/refund-policy")
def get_refund_policy() -> Dict[str, Any]:
    """API Mock cho get_refund_policy tool."""
    return db.policies

@router.post("/tools/ticket", response_model=SupportTicketResponse)
def create_support_ticket(ticket_data: SupportTicketCreate) -> Dict[str, Any]:
    """API Mock cho create_support_ticket tool."""
    res = tool_service.create_support_ticket(
        user_id=ticket_data.user_id,
        category=ticket_data.category,
        description=ticket_data.description
    )
    if res["status"] != "success":
        raise HTTPException(status_code=400, detail=res["message"])
    return res["ticket_details"]
