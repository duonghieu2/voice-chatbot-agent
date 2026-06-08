from typing import Dict, Any, Optional
from app.database.mock_db import db

class ToolService:
    @staticmethod
    def get_ride_status(ride_id: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin trạng thái chuyến xe."""
        return db.get_ride(ride_id)

    @staticmethod
    def cancel_ride(ride_id: str, reason: str = "") -> Dict[str, Any]:
        """Thực hiện hủy chuyến xe và trả về thông tin phí hủy (nếu có)."""
        ride = db.get_ride(ride_id)
        if not ride:
            return {"status": "error", "message": f"Không tìm thấy chuyến xe {ride_id}"}
        
        if ride["status"] in ["completed", "cancelled"]:
            return {
                "status": "error",
                "message": f"Chuyến xe đã ở trạng thái '{ride['status']}', không thể hủy."
            }
        
        # Phạt hủy chuyến 10k nếu tài xế đang đến đón (arriving)
        cancellation_fee = 0
        if ride["status"] in ["accepted", "arriving"]:
            cancellation_fee = 10000
            
        db.update_ride_status(ride_id, "cancelled")
            
        return {
            "status": "success",
            "ride_id": ride_id,
            "message": f"Hủy chuyến xe thành công. Phí hủy chuyến: {cancellation_fee} VND.",
            "cancellation_fee": cancellation_fee
        }

    @staticmethod
    def get_food_order_status(order_id: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin trạng thái đơn hàng đồ ăn."""
        return db.get_food_order(order_id)

    @staticmethod
    def check_payment_status(target_id: str) -> Optional[Dict[str, Any]]:
        """Lấy trạng thái giao dịch thanh toán của chuyến xe hoặc đơn đồ ăn."""
        return db.get_payment_by_target(target_id)

    @staticmethod
    def request_refund(payment_id: str, amount: float, reason: str) -> Dict[str, Any]:
        """Tạo yêu cầu hoàn tiền cho một giao dịch thành công."""
        payment = db.payments.get(payment_id)
        if not payment:
            return {"status": "error", "message": f"Không tìm thấy giao dịch thanh toán {payment_id}"}
        
        if payment["status"] != "success":
            return {"status": "error", "message": f"Giao dịch '{payment_id}' không ở trạng thái thành công."}
            
        if amount > payment["amount"]:
            return {"status": "error", "message": f"Số tiền hoàn ({amount} VND) lớn hơn số tiền giao dịch ({payment['amount']} VND)."}
            
        refund = db.create_refund(payment_id, amount, reason)
        return {
            "status": "success",
            "message": "Tạo yêu cầu hoàn tiền thành công.",
            "refund_details": refund
        }

    @staticmethod
    def create_support_ticket(user_id: str, category: str, description: str) -> Dict[str, Any]:
        """Tạo ticket chuyển tiếp hỗ trợ kỹ thuật hoặc nhân viên chăm sóc khách hàng."""
        ticket = db.create_ticket(user_id, category, description)
        return {
            "status": "success",
            "message": "Tạo phiếu hỗ trợ thành công. Yêu cầu của bạn đã được chuyển tới nhân viên hỗ trợ.",
            "ticket_details": ticket
        }

tool_service = ToolService()
