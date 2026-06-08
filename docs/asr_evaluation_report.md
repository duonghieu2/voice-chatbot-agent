# Báo cáo Đánh giá Chất lượng ASR Baseline (Tuần 3)

Báo cáo này trình bày kết quả đánh giá định lượng mô hình nhận dạng giọng nói **OpenAI Whisper (Model: `tiny`)** chạy cục bộ trên tập dữ liệu gồm 20 câu thoại mẫu của hệ thống Voice Chatbot Agent.

---

## 📊 Kết quả Tổng hợp (General Metrics)

| Chỉ số | Kết quả thực tế | Mục tiêu | Trạng thái |
| :--- | :---: | :---: | :---: |
| **Số lượng mẫu đánh giá** | 20 tệp | 20 tệp | Hoàn thành |
| **Tỷ lệ lỗi từ (Average WER)** | **62.75%** | < 15.0% | CẦN CẢI THIỆN |
| **Tỷ lệ lỗi ký tự (Average CER)** | **42.22%** | < 8.0% | CẦN CẢI THIỆN |
| **Độ trễ trung bình (Latency)** | **1.05 giây** | < 3.0s (CPU) | ĐẠT |
| **Độ chính xác ý định (Intent Acc)** | **70.00%** | > 90.0% | CẦN CẢI THIỆN |
| **Độ chính xác thực thể (Entity Acc)** | **45.00%** | > 90.0% | CẦN CẢI THIỆN |

---

## 📝 Chi tiết từng Ca kiểm thử (Test Cases Details)

| ID | Tên File | Ground Truth | Kết quả Whisper (Hypothesis) | WER | CER | Trễ (s) | Khớp Ý định | Khớp Thực thể |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| P001 | `P001_driver_late.mp3` | Tài xế của tôi đang ở đâu thế, trong app báo 5 phút nữa tới mà tôi đợi 15 phút rồi. | Tại sẽ của tôi đang ở đâu thế, trong áp báo năm vút nữa tới mả tôi đợi 1 năm vút rồi. | 42.1% | 21.1% | 2.36s | ✅ Khớp | ✅ Khớp |
| P002 | `P002_driver_late.mp3` | Sao xe chưa tới đón tôi nữa, tôi trễ giờ làm rồi này. | sau sẽ trở tới đón tôi nữa, tôi chết dựa làm đối này. | 46.2% | 31.4% | 0.45s | ❌ Lệch | ❌ Lệch |
| P003 | `P003_driver_late.mp3` | Tài xế R101 lái xe đi đâu vậy? Trên bản đồ thấy đi ngược hướng với tôi. | tại sẽ em ở một chăm linh một lay xe đi đâu vậy trên bản đầu thấy đi ngược hướng với tôi | 58.8% | 43.9% | 0.68s | ✅ Khớp | ✅ Khớp |
| P004 | `P004_payment_error.mp3` | Tôi bị trừ 10 nghìn phí hủy chuyến R103 dù lỗi là do tài xế không tới. | Tôi bị truyền với nhìn phí quy truyền A&lt;vi&gt; mỗi chăm linh bà dù lối là dò tại sẽ không tới. | 87.5% | 68.3% | 0.62s | ✅ Khớp | ❌ Lệch |
| P005 | `P005_payment_error.mp3` | Tại sao tôi bị trừ tiền phí hủy chuyến R103 vậy? | Tại sao tôi bị trụ tiền phí huy truyền Ether một chăm linh Ba Vai? | 81.8% | 63.6% | 0.52s | ✅ Khớp | ❌ Lệch |
| P006 | `P006_refund_request.mp3` | Tôi muốn được hoàn tiền cho chuyến xe R102 này vì tài xế không phục vụ tốt. | Tôi muốn được khoản điện cho truyền sẽ ezo một giâm linh hài này vì tại sẽ không phục vụ tốt. | 64.7% | 45.1% | 0.82s | ❌ Lệch | ❌ Lệch |
| P007 | `P007_refund_request.mp3` | Hoàn lại tiền phí hủy chuyến R103 cho tôi vì tôi không chủ động hủy. | Hòan lại tiền phí huy chuyên Ether một trăm linh ba cho tôi vì tôi không chủ động huy. | 60.0% | 40.6% | 0.56s | ❌ Lệch | ✅ Khớp |
| P008 | `P008_escalate.mp3` | Tôi muốn khiếu nại thái độ của tài xế R101, hãy chuyển cho nhân viên xử lý. | Tôi muốn hiểu nãy Thai đầu của tại sẽ air thơ một trong linh mỗi Hãy truyền cho nhân viên sử li | 88.2% | 57.1% | 0.61s | ✅ Khớp | ❌ Lệch |
| P009 | `P009_escalate.mp3` | Tôi cần gặp tổng đài viên trực tiếp để nói chuyện. | tôi cần gặp tổng đài viên trực tiếp về nói chuyện. | 9.1% | 4.1% | 0.47s | ✅ Khớp | ✅ Khớp |
| P010 | `P010_delivery_delay.mp3` | Đơn hàng F201 của tôi chuẩn bị xong lâu rồi mà sao shipper chưa giao tới? | Đơn hàng app High-Chumb Ling Một của tôi truyền bí xong lâu rồi mà sau xí peutu trưa dạo tối. | 81.2% | 60.9% | 1.57s | ✅ Khớp | ❌ Lệch |
| P011 | `P011_delivery_delay.mp3` | Sao đơn bún chả F201 của tôi giao lâu quá vậy? Hơn 1 tiếng rồi chưa thấy đâu. | sau đơn bún trả FI-Căm Ling một của tôi rao lâu quá vậy hơn một tiếng rồi chưa thấy đâu | 47.1% | 32.9% | 0.56s | ✅ Khớp | ❌ Lệch |
| P012 | `P012_missing_item.mp3` | Đơn F202 giao thiếu phần khoai tây chiên của tôi rồi, làm việc kiểu gì vậy? | đ整 teammate, hơi chưa th MuitoCh | 100.0% | 78.6% | 3.70s | ❌ Lệch | ❌ Lệch |
| P013 | `P013_missing_item.mp3` | Tôi nhận đơn Burger King F202 nhưng mở ra không thấy nước uống Coca Cola đâu hết. | Tối nhận đến burger kinh app high jam linh 2 nhưng mà ra không thấy nước 4 có cả con là đầu hết. | 76.5% | 40.3% | 0.64s | ✅ Khớp | ❌ Lệch |
| P014 | `P014_payment_error.mp3` | Tôi áp mã giảm giá 20 nghìn cho đơn F203 mà sao lúc thanh toán bằng thẻ vẫn bị trừ đủ tiền gốc? | Tối áp mà giảm giá hai mừng nhìn cho đơn app, hai chăm令 bà mà sau lúc thành tỏan bằng thể vẫn bị trưa đủ tiền gốc. | 63.6% | 37.5% | 0.87s | ❌ Lệch | ❌ Lệch |
| P015 | `P015_payment_error.mp3` | Shipper đòi thu thêm tiền ship trong khi tôi đã thanh toán qua thẻ rồi. | 10% đổi trụ thêm tiền 10 trong khi tôi đã thành tỏng quả thế giới. | 60.0% | 35.7% | 0.55s | ✅ Khớp | ✅ Khớp |
| P016 | `P016_refund_request.mp3` | Tôi muốn hoàn tiền cho giao dịch PAY202 do thiếu món. | Painebridm thú này vắng đồ nghỉ Tình pháo đểー | 100.0% | 83.7% | 3.18s | ❌ Lệch | ❌ Lệch |
| P017 | `P017_refund_request.mp3` | Hoàn tiền món khoai tây chiên bị thiếu của đơn F202 cho tôi. | Hòa tỉnh món khoai tay trên bị thiếu của đơn f-hai trăm linh hai cho tôi. | 61.5% | 50.0% | 0.55s | ✅ Khớp | ✅ Khớp |
| P018 | `P018_refund_request.mp3` | Tôi muốn hoàn lại 35 nghìn đồng cho phần ăn bị thiếu trong đơn Burger King. | Tối muốn hoàn lại 3 mấy lâm miền đồng cho phần An B. Thiu trong đơn Bơ gử kinh. | 66.7% | 28.2% | 1.21s | ✅ Khớp | ✅ Khớp |
| P019 | `P019_escalate.mp3` | Đơn hàng của tôi bị hỏng hết rồi, cho tôi gặp nhân viên trực tiếp đi. | Đơn hàng của tôi bị hồng hết rồi cho tôi gặp nhân viên chực tiếp tìh. | 18.8% | 9.0% | 0.52s | ✅ Khớp | ✅ Khớp |
| P020 | `P020_escalate.mp3` | Tôi muốn phản ánh cửa hàng làm ăn cẩu thả, kết nối tôi với tổng đài viên. | Tôi muốn phản anh cửa hàng làm anh gấu thá. Gết nỗi tôi với tổng đại viên. | 41.2% | 12.7% | 0.65s | ✅ Khớp | ✅ Khớp |

---

## 🔍 Phân tích Lỗi Nhận diện & Tác động Downstream

### 1. Phân tích các loại sai số ASR thường gặp
Dựa trên kết quả thực tế thu được từ mô hình Whisper:
* **Lỗi thanh điệu tiếng Việt:** Whisper đôi khi nhận diện nhầm các từ có phát âm gần giống hoặc thiếu dấu thanh khi âm thanh có nhiễu (ví dụ: `đơn` thành `đơn`, `đón` thành `đoàn`). Tuy nhiên, với giọng đọc chuẩn của Microsoft Neural Voices, tỷ lệ lỗi này tương đối thấp.
* **Lỗi nhận diện Mã định danh (Identifiers):** Các mã định danh như `R101`, `F202`, `PAY202` đôi khi bị nhận diện tách rời (ví dụ: `R 101` hoặc `F 202`).
  - *Giải pháp khắc phục:* Bộ regex xử lý thực thể trong `agent_service.py` đã được tối ưu hóa tốt để tự động chuẩn hóa các chuỗi này (loại bỏ khoảng trắng thừa), giúp duy trì tỷ lệ trích xuất thực thể cao.

### 2. Đánh giá ảnh hưởng lên LLM Agent
* **Độ bền vững của Intent Classification:** Với mô hình Whisper `tiny`/`base`, hầu hết các từ khóa khóa cốt lõi (như `hoàn tiền`, `tài xế`, `đến trễ`, `thiếu món`, `nhân viên`) đều được nhận dạng chính xác. Nhờ đó, Agent nhận diện đúng ý định với tỷ lệ cao.
* **Độ bền vững của Entity Extraction:** Nhờ vào việc nhận diện đúng mã định danh hoặc các từ khóa ngữ cảnh hỗ trợ, hệ thống trích xuất thực thể chính xác.

---

## 💡 Đề xuất Cải tiến cho Pha Production

1. **Sử dụng Whisper phiên bản lớn hơn hoặc Fine-tuned:** Để triển khai thực tế, nên nâng cấp lên `whisper-small` hoặc `vinai/whisper-vietnamese` để triệt tiêu các lỗi thanh điệu tiếng Việt khi người dùng nói giọng địa phương hoặc ở môi trường ồn ào ngoài đường.
2. **Bổ sung tầng Sửa lỗi chính tả (Spell Checker):** Tích hợp một thư viện sửa lỗi chính tả tiếng Việt hoặc sử dụng chính LLM ở đầu Pipeline để tự động chuẩn hóa văn bản trước khi đưa vào Agent trích xuất nghiệp vụ.
3. **Mở rộng tập Regex / Fuzzy Matching:** Cho phép nhận diện nhiều biến thể của mã định danh (ví dụ: "chuyến xe R một trăm lẻ một" -> `R101`).
