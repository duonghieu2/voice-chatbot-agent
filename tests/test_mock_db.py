import pytest
from app.database.mock_db import db

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Reset database trước mỗi case test để đảm bảo tính độc lập
    db.reset_db()
    yield

def test_get_ride():
    ride = db.get_ride("R101")
    assert ride is not None
    assert ride["driver_name"] == "Lê Văn C"
    assert ride["status"] == "arriving"

    non_exist_ride = db.get_ride("R999")
    assert non_exist_ride is None

def test_update_ride_status():
    success = db.update_ride_status("R101", "cancelled")
    assert success is True
    ride = db.get_ride("R101")
    assert ride["status"] == "cancelled"

    fail = db.update_ride_status("R999", "cancelled")
    assert fail is False

def test_get_food_order():
    order = db.get_food_order("F201")
    assert order is not None
    assert order["restaurant_name"] == "Bún Chả Sinh Từ"
    assert order["status"] == "preparing"
    assert order["subtotal"] == 130000

def test_update_food_order_status():
    success = db.update_food_order_status("F201", "completed")
    assert success is True
    order = db.get_food_order("F201")
    assert order["status"] == "completed"

def test_get_payment_by_target():
    payment = db.get_payment_by_target("R102")
    assert payment is not None
    assert payment["id"] == "PAY102"
    assert payment["amount"] == 80000

def test_create_refund():
    # Tạo refund cho PAY202
    refund = db.create_refund("PAY202", 35000.0, "Thiếu món")
    assert refund["id"].startswith("REF")
    assert refund["payment_id"] == "PAY202"
    assert refund["amount"] == 35000.0
    assert refund["status"] == "pending"
    assert refund["id"] in db.refunds

def test_create_ticket():
    ticket = db.create_ticket("U001", "ride_issue", "Tài xế lái ẩu")
    assert ticket["id"].startswith("TKT")
    assert ticket["user_id"] == "U001"
    assert ticket["status"] == "open"
    assert ticket["id"] in db.tickets
