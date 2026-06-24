TOOL_DEFINITIONS = [
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
    },
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
    },
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
    },
    {
      "name": "get_refund_policy",
      "description": "Truy xuất chính sách hoàn tiền cho món ăn thiếu, quy định phạt phí hủy chuyến xe, và SLA cam kết hỗ trợ khách hàng của nền tảng.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
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
            "description": "Danh mục khiếu nại. Lựa chọn trong: 'ride_issue' (vấn đề đặt xe), 'food_issue' (vấn đề đồ ăn), 'payment_issue' (vấn đề cước phí/thanh toán), hoặc 'other'."
          },
          "description": {
            "type": "string",
            "description": "Mô tả chi tiết nội dung khiếu nại của khách hàng (ví dụ: 'Tài xế lái ẩu', 'Shipper giao thiếu trà sữa')."
          }
        },
        "required": ["user_id", "category", "description"]
      }
    },
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
]
