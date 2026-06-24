# Đặc tả Kỹ thuật Cấu trúc Tool Calling (FastAPI & LLM Integration)

Tài liệu này thuyết minh chi tiết cấu trúc định nghĩa công cụ (Tool Calling Specifications) phục vụ tích hợp mô hình ngôn ngữ lớn (LLM) và cung cấp tài liệu API cho các Mock API của từng công cụ trên hệ thống **Voice Chatbot Agent**.

---

## 1. Danh sách Định nghĩa JSON Schema của 6 Tools cốt lõi

Các công cụ được thiết kế theo định dạng chuẩn tương thích với cơ chế Tool Calling của OpenAI và Gemini API. Các đặc tả này được cung cấp trực tuyến tại Endpoint `/api/v1/tools/definitions`.

### Tool 1: `check_ride_status`
- **Mô tả:** Tra cứu trạng thái và thông tin hành trình của chuyến xe (tài xế, biển số, điểm đón, điểm trả, ETA).
- **Schema định nghĩa:**
```json
{
  "name": "check_ride_status",
  "description": "Tra cứu thông tin chi tiết và trạng thái hiện tại của chuyến xe (tên tài xế, biển số xe, ETA đón khách, trạng thái thanh toán, điểm đi/đến).",
  "parameters": {
    "type": "object",
    "properties": {
      "ride_id": {
        "type": "string",
        "description": "Mã định danh chuyến xe cần tra cứu, định dạng Rxxx (ví dụ: R101)."
      }
    },
    "required": ["ride_id"]
  }
}
```

### Tool 2: `check_order_status`
- **Mô tả:** Tra cứu thông tin đơn đồ ăn, các món ăn đặt mua và danh sách các món bị giao thiếu (nếu có).
- **Schema định nghĩa:**
```json
{
  "name": "check_order_status",
  "description": "Tra cứu thông tin chi tiết và trạng thái của đơn hàng đồ ăn (tên cửa hàng/nhà hàng, danh sách món ăn, trạng thái chuẩn bị/giao hàng, danh sách món bị giao thiếu).",
  "parameters": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "Mã định danh đơn hàng cần tra cứu, định dạng Fxxx (ví dụ: F202)."
      }
    },
    "required": ["order_id"]
  }
}
```

### Tool 3: `verify_billing_fees`
- **Mô tả:** Xác thực hóa đơn, số tiền giao dịch và phương thức thanh toán của đơn ăn hoặc chuyến xe.
- **Schema định nghĩa:**
```json
{
  "name": "verify_billing_fees",
  "description": "Tra cứu thông tin giao dịch thanh toán, hóa đơn, cước phí của chuyến xe hoặc đơn hàng đồ ăn.",
  "parameters": {
    "type": "object",
    "properties": {
      "target_id": {
        "type": "string",
        "description": "Mã định danh của chuyến xe (Rxxx) hoặc đơn hàng đồ ăn (Fxxx) liên quan tới giao dịch cần kiểm tra."
      }
    },
    "required": ["target_id"]
  }
}
```

### Tool 4: `get_refund_policy`
- **Mô tả:** Truy xuất các quy chế chính sách bồi hoàn, phạt hủy chuyến xe, và SLA cam kết hỗ trợ khách hàng.
- **Schema định nghĩa:**
```json
{
  "name": "get_refund_policy",
  "description": "Truy xuất chính sách hoàn tiền cho món ăn thiếu, quy định phạt phí hủy chuyến xe, và SLA cam kết hỗ trợ khách hàng của nền tảng.",
  "parameters": {
    "type": "object",
    "properties": {}
  }
}
```

### Tool 5: `create_support_ticket`
- **Mô tả:** Tạo phiếu hỗ trợ chuyển tiếp khiếu nại chưa xử lý được ngay sang nhân viên hỗ trợ trực tiếp.
- **Schema định nghĩa:**
```json
{
  "name": "create_support_ticket",
  "description": "Tạo phiếu hỗ trợ cứu trợ kỹ thuật hoặc khiếu nại khách hàng để chuyển tiếp xử lý trực tiếp bởi tổng đài viên/nhân sự chuyên trách.",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "Mã định danh của khách hàng yêu cầu khiếu nại (ví dụ: U001)."
      },
      "category": {
        "type": "string",
        "description": "Danh mục khiếu nại. Lựa chọn trong: 'ride_issue', 'food_issue', 'payment_issue', hoặc 'other'."
      },
      "description": {
        "type": "string",
        "description": "Mô tả chi tiết nội dung khiếu nại của khách hàng (ví dụ: 'Tài xế lái ẩu', 'Shipper giao thiếu trà sữa')."
      }
    },
    "required": ["user_id", "category", "description"]
  }
}
```

### Tool 6: `request_refund`
- **Mô tả:** Tạo yêu cầu hoàn tiền cho một giao dịch thanh toán bị sự cố hoặc thiếu món.
- **Schema định nghĩa:**
```json
{
  "name": "request_refund",
  "description": "Tạo yêu cầu hoàn tiền cho một giao dịch thanh toán bị sự cố hoặc thiếu món.",
  "parameters": {
    "type": "object",
    "properties": {
      "payment_id": {
        "type": "string",
        "description": "Mã định danh giao dịch thanh toán cần hoàn tiền, định dạng PAYxxx (ví dụ: PAY202)."
      },
      "amount": {
        "type": "number",
        "description": "Số tiền hoàn (ví dụ: 35000.0)."
      },
      "reason": {
        "type": "string",
        "description": "Lý do hoàn tiền (ví dụ: 'Giao thiếu món khoai tây chiên cỡ lớn')."
      }
    },
    "required": ["payment_id", "amount", "reason"]
  }
}
```

---

## 2. API Endpoints của Mock Tools trên FastAPI Backend

FastAPI Backend hỗ trợ gọi các mock tool trực tuyến thông qua REST API dưới prefix `/api/v1`:

| STT | Endpoint | Phương thức | Dữ liệu trả về (Mock JSON) |
| :--- | :--- | :---: | :--- |
| 1 | `/tools/definitions` | `GET` | Bản kê JSON Schema của cả 6 tools. |
| 2 | `/tools/ride-status/{ride_id}` | `GET` | Bản ghi chuyến xe trong `rides` (mã HTTP 404 nếu không tồn tại). |
| 3 | `/tools/order-status/{order_id}` | `GET` | Bản ghi đơn hàng trong `food_orders` (mã HTTP 404 nếu không tồn tại). |
| 4 | `/tools/billing-fees/{target_id}` | `GET` | Bản ghi hóa đơn giao dịch trong `payments` (mã HTTP 404 nếu không tồn tại). |
| 5 | `/tools/refund-policy` | `GET` | Bộ điều khoản quy định hoàn phí trong `policies`. |
| 6 | `/tools/ticket` | `POST` | Bản ghi ticket mới được tạo thành công trong `tickets`. |
