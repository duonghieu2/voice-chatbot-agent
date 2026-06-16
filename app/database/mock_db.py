import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class MockDatabase:
    def __init__(self):
        # Xác định đường dẫn tới mock_backend_data.json
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(current_dir, "mock_backend_data.json")
        
        # Load seed dữ liệu ban đầu từ file JSON để làm mốc khôi phục
        self._seed_data = self._load_from_file()
        
        # Thiết lập các biến database in-memory
        self.reset_db()

    def _load_from_file(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                print(f"Warning: File {self.data_path} không tồn tại.")
        except Exception as e:
            print(f"Lỗi khi đọc file mock_backend_data.json: {e}")
        
        # Fallback cấu trúc rỗng
        return {
            "users": {},
            "rides": {},
            "food_orders": {},
            "payments": {},
            "refunds": {},
            "tickets": {},
            "policies": {}
        }

    def _save_db(self):
        """Ghi ngược trạng thái hiện tại in-memory xuống file đĩa JSON."""
        # Không ghi xuống đĩa nếu đang chạy trong môi trường test, script đánh giá hoặc luồng tĩnh
        import sys
        main_script = os.path.basename(sys.argv[0]) if sys.argv else ""
        if "pytest" in sys.modules or "evaluate_asr.py" in main_script or "test_static_flow.py" in main_script or "test_end_to_end.py" in main_script:
            return
            
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump({
                    "users": self.users,
                    "rides": self.rides,
                    "food_orders": self.food_orders,
                    "payments": self.payments,
                    "refunds": self.refunds,
                    "tickets": self.tickets,
                    "policies": self.policies
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu DB xuống đĩa: {e}")

    def reset_db(self):
        """Khôi phục bộ nhớ in-memory và tệp đĩa về trạng thái hạt giống (clean seed) ban đầu."""
        # Deep copy dữ liệu hạt giống sang các bảng in-memory
        self.users = json.loads(json.dumps(self._seed_data.get("users", {})))
        self.rides = json.loads(json.dumps(self._seed_data.get("rides", {})))
        self.food_orders = json.loads(json.dumps(self._seed_data.get("food_orders", {})))
        self.payments = json.loads(json.dumps(self._seed_data.get("payments", {})))
        self.refunds = json.loads(json.dumps(self._seed_data.get("refunds", {})))
        self.tickets = json.loads(json.dumps(self._seed_data.get("tickets", {})))
        self.policies = json.loads(json.dumps(self._seed_data.get("policies", {})))
        
        # Ghi ngược lại đĩa để tệp đĩa luôn ở trạng thái sạch trước mỗi test
        self._save_db()

    # --- Các phương thức truy vấn và cập nhật dữ liệu ---

    def get_ride(self, ride_id: str) -> Optional[Dict[str, Any]]:
        return self.rides.get(ride_id)

    def update_ride_status(self, ride_id: str, status: str) -> bool:
        if ride_id in self.rides:
            self.rides[ride_id]["status"] = status
            self._save_db()
            return True
        return False

    def get_food_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        return self.food_orders.get(order_id)

    def update_food_order_status(self, order_id: str, status: str) -> bool:
        if order_id in self.food_orders:
            self.food_orders[order_id]["status"] = status
            self._save_db()
            return True
        return False

    def get_payment_by_target(self, target_id: str) -> Optional[Dict[str, Any]]:
        for pay in self.payments.values():
            if pay["target_id"] == target_id:
                return pay
        return None

    def create_refund(self, payment_id: str, amount: float, reason: str) -> Dict[str, Any]:
        refund_id = f"REF{len(self.refunds) + 501}"
        refund_data = {
            "id": refund_id,
            "payment_id": payment_id,
            "amount": amount,
            "reason": reason,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self.refunds[refund_id] = refund_data
        self._save_db()
        return refund_data

    def create_ticket(self, user_id: str, category: str, description: str) -> Dict[str, Any]:
        ticket_id = f"TKT{len(self.tickets) + 801}"
        ticket_data = {
            "id": ticket_id,
            "user_id": user_id,
            "category": category,
            "description": description,
            "status": "open",
            "created_at": datetime.now().isoformat()
        }
        self.tickets[ticket_id] = ticket_data
        self._save_db()
        return ticket_data

# Khởi tạo instance database dùng chung toàn ứng dụng
db = MockDatabase()
