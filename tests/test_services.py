import pytest
from app.database.mock_db import db
from app.services.tool_service import tool_service
from app.services.asr_service import asr_service
from app.services.agent_service import agent_service

@pytest.fixture(autouse=True)
def setup_db():
    db.reset_db()
    yield

def test_tool_service_cancel_ride():
    # Hủy chuyến xe R101 (đang đến -> được phép hủy, phí hủy 10k)
    res = tool_service.cancel_ride("R101", "Tôi không muốn đi nữa")
    assert res["status"] == "success"
    assert res["cancellation_fee"] == 10000
    assert db.get_ride("R101")["status"] == "cancelled"

    # Thử hủy lại chuyến xe đã hủy
    res_retry = tool_service.cancel_ride("R101")
    assert res_retry["status"] == "error"
    assert "không thể hủy" in res_retry["message"]

def test_tool_service_request_refund():
    # Hoàn tiền thành công
    res = tool_service.request_refund("PAY202", 35000.0, "Thiếu món")
    assert res["status"] == "success"
    assert "refund_details" in res
    assert res["refund_details"]["amount"] == 35000.0

    # Hoàn tiền vượt mức giao dịch gốc (PAY202 là 164000)
    res_fail = tool_service.request_refund("PAY202", 200000.0, "Đòi nhiều hơn")
    assert res_fail["status"] == "error"
    assert "lớn hơn số tiền giao dịch" in res_fail["message"]

def test_asr_service():
    # Test ánh xạ giọng nói sang chữ viết
    t1 = asr_service.transcribe(b"", "tai_xe_den_tre.wav")
    assert t1 == "Tài xế của tôi đang ở đâu thế, trong app báo 5 phút nữa tới mà tôi đợi 15 phút rồi."

    t2 = asr_service.transcribe(b"", "giao_thieu_mon.wav")
    assert t2 == "Đơn F202 giao thiếu phần khoai tây chiên của tôi rồi, làm việc kiểu gì vậy?"

    t3 = asr_service.transcribe(b"", "random.wav")
    assert t3 == "Chào bạn, tôi cần kiểm tra trạng thái đơn hàng"

def test_agent_service_ride_late():
    result = agent_service.process_transcript("Tôi muốn khiếu nại tài xế R101 đến trễ quá")
    assert result["intent"] == "check_ride_status"
    assert result["tool_called"] == "get_ride_status"
    assert result["tool_args"] == {"ride_id": "R101"}
    assert "Lê Văn C" in result["agent_response"]
    assert "29A-12345" in result["agent_response"]

def test_agent_service_missing_food():
    result = agent_service.process_transcript("Đơn hàng F202 của tôi giao bị thiếu món khoai tây chiên")
    assert result["intent"] == "check_food_order_status"
    assert result["tool_called"] == "get_food_order_status"
    assert "Burger King - Bà Triệu" in result["agent_response"]
    assert "Khoai tây chiên cỡ lớn" in result["agent_response"]

def test_agent_service_cancel_fee():
    result = agent_service.process_transcript("Tại sao tôi bị trừ tiền phí hủy chuyến R103 vậy")
    assert result["intent"] == "check_ride_cancellation_fee"
    assert result["tool_called"] == "get_ride_status"
    assert "áp dụng phí hủy chuyến" in result["agent_response"]

def test_agent_service_refund():
    result = agent_service.process_transcript("Tôi muốn hoàn tiền cho giao dịch PAY202 do thiếu món")
    assert result["intent"] == "request_refund"
    assert result["tool_called"] == "request_refund"
    assert result["tool_args"]["payment_id"] == "PAY202"
    assert "35,000 VND" in result["agent_response"]

def test_agent_service_escalation():
    result = agent_service.process_transcript("Gặp nhân viên hỗ trợ giúp tôi gấp")
    assert result["intent"] == "escalate_to_support"
    assert result["tool_called"] == "create_support_ticket"
    assert "đã tiếp nhận khiếu nại" in result["agent_response"]
    assert len(db.tickets) == 3
