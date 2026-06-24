from fastapi.testclient import TestClient
import io
from app.main import app
from app.database.mock_db import db

import os

client = TestClient(app)
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio_samples")

def setup_function():
    # Reset DB trước mỗi API test
    db.reset_db()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Voice Chatbot Agent API đang hoạt động ổn định!"}

def test_voice_endpoint_driver_late():
    # Sử dụng tệp âm thanh thực tế được sinh ở bước trước
    audio_path = os.path.join(AUDIO_DIR, "P001_driver_late.mp3")
    assert os.path.exists(audio_path), f"File {audio_path} không tồn tại!"
    
    with open(audio_path, "rb") as f:
        response = client.post(
            "/api/v1/chatbot/voice",
            files={"file": ("P001_driver_late.mp3", f, "audio/mpeg")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["file_name"] == "P001_driver_late.mp3"
    assert "pipeline_results" in data
    
    results = data["pipeline_results"]
    assert results["asr_transcript"] == "Tài xế của tôi đang ở đâu thế, trong app báo 5 phút nữa tới mà tôi đợi 15 phút rồi."
    assert results["intent"] == "check_ride_status"
    assert results["tool_called"] == "get_ride_status"
    assert results["tool_args"] == {"ride_id": "R101"}
    assert "Lê Văn C" in results["agent_response"]

def test_voice_endpoint_missing_food():
    audio_path = os.path.join(AUDIO_DIR, "P012_missing_item.mp3")
    assert os.path.exists(audio_path), f"File {audio_path} không tồn tại!"
    
    with open(audio_path, "rb") as f:
        response = client.post(
            "/api/v1/chatbot/voice",
            files={"file": ("P012_missing_item.mp3", f, "audio/mpeg")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "pipeline_results" in data
    
    results = data["pipeline_results"]
    assert results["asr_transcript"] == "Đơn F202 giao thiếu phần khoai tây chiên của tôi rồi, làm việc kiểu gì vậy?"
    assert results["intent"] == "check_food_order_status"
    assert "Burger King - Bà Triệu" in results["agent_response"]
    assert "Khoai tây chiên cỡ lớn" in results["agent_response"]

def test_voice_endpoint_refund():
    audio_path = os.path.join(AUDIO_DIR, "P016_refund_request.mp3")
    assert os.path.exists(audio_path), f"File {audio_path} không tồn tại!"
    
    with open(audio_path, "rb") as f:
        response = client.post(
            "/api/v1/chatbot/voice",
            files={"file": ("P016_refund_request.mp3", f, "audio/mpeg")}
        )
    
    assert response.status_code == 200
    data = response.json()
    
    results = data["pipeline_results"]
    assert results["intent"] == "request_refund"
    assert results["tool_called"] == "request_refund"
    assert "PAY202" in results["agent_response"]
    assert "35,000" in results["agent_response"]

# --- Kiểm thử các endpoint của Tool Calling ---

def test_get_tool_definitions():
    response = client.get("/api/v1/tools/definitions")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) == 6
    tool_names = [t["name"] for t in data["tools"]]
    assert "check_ride_status" in tool_names
    assert "create_support_ticket" in tool_names
    assert "request_refund" in tool_names

def test_check_ride_status_endpoint():
    response = client.get("/api/v1/tools/ride-status/R101")
    assert response.status_code == 200
    data = response.json()
    assert data["driver_name"] == "Lê Văn C"
    assert data["status"] == "arriving"

    # Case lowercase ID
    response_lower = client.get("/api/v1/tools/ride-status/r101")
    assert response_lower.status_code == 200

    # Case 404
    response_404 = client.get("/api/v1/tools/ride-status/R999")
    assert response_404.status_code == 404

def test_check_order_status_endpoint():
    response = client.get("/api/v1/tools/order-status/F201")
    assert response.status_code == 200
    data = response.json()
    assert data["restaurant_name"] == "Bún Chả Sinh Từ"
    assert data["status"] == "preparing"

    # Case 404
    response_404 = client.get("/api/v1/tools/order-status/F999")
    assert response_404.status_code == 404

def test_verify_billing_fees_endpoint():
    response = client.get("/api/v1/tools/billing-fees/R102")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "PAY102"
    assert data["amount"] == 80000

    # Case 404
    response_404 = client.get("/api/v1/tools/billing-fees/R999")
    assert response_404.status_code == 404

def test_get_refund_policy_endpoint():
    response = client.get("/api/v1/tools/refund-policy")
    assert response.status_code == 200
    data = response.json()
    assert "ride_cancellation_fee" in data
    assert data["ride_cancellation_fee"] == 10000

def test_create_support_ticket_endpoint():
    payload = {
        "user_id": "U001",
        "category": "ride_issue",
        "description": "Tài xế lái ẩu trên cao tốc"
    }
    response = client.post("/api/v1/tools/ticket", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("TKT")
    assert data["status"] == "open"
    assert data["user_id"] == "U001"

def test_request_refund_endpoint():
    payload = {
        "payment_id": "PAY202",
        "amount": 35000.0,
        "reason": "Giao thiếu khoai tây chiên"
    }
    response = client.post("/api/v1/tools/refund", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "refund_details" in data
    assert data["refund_details"]["payment_id"] == "PAY202"
    assert data["refund_details"]["amount"] == 35000.0

