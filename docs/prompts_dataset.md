# Tài liệu Thiết kế Tập dữ liệu Câu thoại Mẫu (Text Prompts Dataset)

Tài liệu này thuyết minh thiết kế, phân loại và hướng dẫn sử dụng tập dữ liệu câu thoại mẫu (Text Prompts) giả lập ý kiến khiếu nại của người dùng trong hệ thống **Voice Chatbot Agent**.

---

## 1. Tổng quan & Thiết kế Cấu trúc
Tập dữ liệu câu thoại được lưu trữ tại [prompts.json](file:///c:/Users/Administrator/Developer/Intern_VSF/voice-chatbot-agent/app/database/prompts.json) dưới định dạng JSON có cấu trúc. Mỗi câu thoại đại diện cho một thông điệp thoại bằng tiếng Việt tự nhiên và được chú giải đầy đủ:

- `id`: Mã định danh duy nhất (từ `P001` đến `P020`).
- `domain`: Lĩnh vực nghiệp vụ (`ride` - Đặt xe, `food` - Đặt đồ ăn).
- `category`: Danh mục khiếu nại (`driver_late`, `missing_item`, `delivery_delay`, `payment_error`, `refund_request`, `escalate`).
- `text`: Nội dung câu nói thực tế của người dùng.
- `expected_intent`: Ý định dự kiến mà Agent cần trích xuất.
- `expected_entities`: Danh sách các thực thể (như mã ID, tên món) mà Agent cần nhận diện.

---

## 2. Thống kê Phân bổ Dữ liệu
Tập dữ liệu gồm **20 câu thoại mẫu** phân bố đều cho cả hai lĩnh vực dịch vụ chính:

| Domain (Lĩnh vực) | Category (Danh mục lỗi) | Số lượng câu thoại | Tỷ lệ (%) |
| :--- | :--- | :--- | :--- |
| **Đặt xe (Ride-hailing)** | Tài xế đến đón muộn (`driver_late`) | 3 | 15% |
| | Lỗi cước phí / Phí hủy xe (`payment_error`) | 2 | 10% |
| | Đòi hoàn tiền chuyến xe (`refund_request`) | 2 | 10% |
| | Chuyển hỗ trợ / Khiếu nại thái độ (`escalate`) | 2 | 10% |
| **Đặt đồ ăn (Food)** | Shipper giao hàng trễ (`delivery_delay`) | 2 | 10% |
| | Nhà hàng giao thiếu món (`missing_item`) | 2 | 10% |
| | Lỗi khuyến mãi / Cước phí (`payment_error`) | 2 | 10% |
| | Yêu cầu hoàn trả tiền món thiếu (`refund_request`) | 3 | 15% |
| | Đồ ăn hỏng / Khiếu nại cửa hàng (`escalate`) | 2 | 10% |
| **Tổng cộng** | | **20** | **100%** |

---

## 3. Phân loại Câu thoại Chi tiết theo Domain

### Domain 1: Đặt xe (Ride-hailing)
Tập trung vào các vấn đề di chuyển, tương tác với tài xế và cước phí chuyến đi:
1. **Tài xế đến đón muộn:**
   - *"Tài xế của tôi đang ở đâu thế, trong app báo 5 phút nữa tới mà tôi đợi 15 phút rồi."* (Mã: `P001`)
   - *"Sao xe chưa tới đón tôi nữa, tôi trễ giờ làm rồi này."* (Mã: `P002`)
   - *"Tài xế R101 lái xe đi đâu vậy? Trên bản đồ thấy đi ngược hướng với tôi."* (Mã: `P003`)
2. **Lỗi cước phí / Hủy chuyến:**
   - *"Tôi bị trừ 10 nghìn phí hủy chuyến R103 dù lỗi là do tài xế không tới."* (Mã: `P004`)
   - *"Tại sao tôi bị trừ tiền phí hủy chuyến R103 vậy?"* (Mã: `P005`)
3. **Yêu cầu hoàn tiền:**
   - *"Tôi muốn được hoàn tiền cho chuyến xe R102 này vì tài xế không phục vụ tốt."* (Mã: `P006`)
   - *"Hoàn lại tiền phí hủy chuyến R103 cho tôi vì tôi không chủ động hủy."* (Mã: `P007`)
4. **Chuyển nhân viên hỗ trợ:**
   - *"Tôi muốn khiếu nại thái độ của tài xế R101, hãy chuyển cho nhân viên xử lý."* (Mã: `P008`)
   - *"Tôi cần gặp tổng đài viên trực tiếp để nói chuyện."* (Mã: `P009`)

### Domain 2: Đặt đồ ăn (Food Delivery)
Tập trung vào chất lượng chuẩn bị món ăn, shipper giao đồ và chính sách bồi hoàn món bị thiếu:
1. **Giao đồ ăn muộn:**
   - *"Đơn hàng F201 của tôi chuẩn bị xong lâu rồi mà sao shipper chưa giao tới?"* (Mã: `P010`)
   - *"Sao đơn bún chả F201 của tôi giao lâu quá vậy? Hơn 1 tiếng rồi chưa thấy đâu."* (Mã: `P011`)
2. **Giao thiếu món:**
   - *"Đơn F202 giao thiếu phần khoai tây chiên của tôi rồi, làm việc kiểu gì vậy?"* (Mã: `P012`)
   - *"Tôi nhận đơn Burger King F202 nhưng mở ra không thấy nước uống Coca Cola đâu hết."* (Mã: `P013`)
3. **Lỗi thanh toán / Khuyến mãi:**
   - *"Tôi áp mã giảm giá 20 nghìn cho đơn F203 mà sao lúc thanh toán bằng thẻ vẫn bị trừ đủ tiền gốc?"* (Mã: `P014`)
   - *"Shipper đòi thu thêm tiền ship trong khi tôi đã thanh toán qua thẻ rồi."* (Mã: `P015`)
4. **Yêu cầu hoàn tiền:**
   - *"Tôi muốn hoàn tiền cho giao dịch PAY202 do thiếu món."* (Mã: `P016`)
   - *"Hoàn tiền món khoai tây chiên bị thiếu của đơn F202 cho tôi."* (Mã: `P017`)
   - *"Tôi muốn hoàn lại 35 nghìn đồng cho phần ăn bị thiếu trong đơn Burger King."* (Mã: `P018`)
5. **Chuyển nhân viên hỗ trợ:**
   - *"Đơn hàng của tôi bị hỏng hết rồi, cho tôi gặp nhân viên trực tiếp đi."* (Mã: `P019`)
   - *"Tôi muốn phản ánh cửa hàng làm ăn cẩu thả, kết nối tôi với tổng đài viên."* (Mã: `P020`)

---

## 4. Tích hợp và Sử dụng
- **ASR Service:** Đọc tệp dữ liệu này để thực hiện mô phỏng nhận dạng giọng nói từ xa (mock voice transcription) dựa trên từ khóa khớp trong tên file.
- **LLM Agent Pipeline:** Nhận văn bản thô trực tiếp từ bộ dữ liệu để đánh giá tỷ lệ trích xuất đúng ý định (Intent Classification Accuracy) và gọi đúng API tương ứng của Mock DB.
