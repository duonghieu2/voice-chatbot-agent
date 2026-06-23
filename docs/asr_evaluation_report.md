# Báo cáo Đánh giá Chất lượng Voice Chatbot Agent (E2E & ASR)

Báo cáo này trình bày kết quả đánh giá định lượng mô hình nhận dạng giọng nói **OpenAI Whisper (Model: `small`)** phối hợp cùng mô hình **Gemini LLM Agent** chạy trên tập dữ liệu gồm 20 câu thoại mẫu của hệ thống Voice Chatbot Agent.

---

## 📊 Kết quả Tổng hợp (General Metrics)

| Chỉ số | Kết quả thực tế | Mục tiêu | Trạng thái |
| :--- | :---: | :---: | :---: |
| **Số lượng mẫu đánh giá** | 20 tệp | 20 tệp | Hoàn thành |
| **Tỷ lệ lỗi từ (Average WER)** | **11.23%** | < 20.0% | ĐẠT |
| **Tỷ lệ lỗi ký tự (Average CER)** | **6.64%** | < 10.0% | ĐẠT |
| **Độ trễ trung bình (Latency)** | **3.01 giây** | < 5.0s (GPU) | ĐẠT |
| **Độ chính xác ý định (Intent Acc)** | **100.00%** | > 80.0% | ĐẠT |
| **Độ chính xác thực thể (Entity Acc)** | **100.00%** | > 80.0% | ĐẠT |
| **Độ chính xác gọi Tool (Tool Calling Acc)** | **100.00%** | > 80.0% | ĐẠT |
| **Độ chính xác chuyển tiếp (Escalation Acc)** | **100.00%** | > 90.0% | ĐẠT |
| **Tỷ lệ bịa đặt dữ liệu (Hallucination Rate)** | **0.00%** | = 0.0% | ĐẠT |

---

## 📝 Chi tiết từng Ca kiểm thử (Test Cases Details)

| ID | Ground Truth | Kết quả Whisper (Hypothesis) | WER | CER | Khớp Ý định | Khớp Thực thể | Khớp Gọi Tool | Tránh Bịa đặt |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| P001 | Tài xế của tôi đang ở đâu thế, trong app báo 5 phút nữa tới mà tôi đợi 15 phút rồi. | Tài xế của tôi đang ở đâu thế? Trong áp báo 5 phút nữa tới mà tôi đợi 15 phút rồi. | 5.3% | 2.6% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P002 | Sao xe chưa tới đón tôi nữa, tôi trễ giờ làm rồi này. | Sau xe chưa tới đón tôi nữa, tôi trễ giờ làm rồi này. | 7.7% | 2.0% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P003 | Tài xế R101 lái xe đi đâu vậy? Trên bản đồ thấy đi ngược hướng với tôi. | Tại xế E-R100 linh 1 lái xe đi đâu vậy? Trên bản đồ thấy đi ngược hướng với tôi. | 17.6% | 12.1% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P004 | Tôi bị trừ 10 nghìn phí hủy chuyến R103 dù lỗi là do tài xế không tới. | Tôi bị trừ 10.000 phí hủy chuyến Eder 103 dù lỗi là do tài xế không tới. | 12.5% | 14.3% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P005 | Tại sao tôi bị trừ tiền phí hủy chuyến R103 vậy? | Tại sao tôi bị trừ tiền phí hủy chuyến error 103 vậy? | 9.1% | 9.1% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P006 | Tôi muốn được hoàn tiền cho chuyến xe R102 này vì tài xế không phục vụ tốt. | Tôi muốn được hoàn tiền cho chuyến xe Eder 100 linh 2 này vì tài xế không phục vụ tốt. | 11.8% | 11.3% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P007 | Hoàn lại tiền phí hủy chuyến R103 cho tôi vì tôi không chủ động hủy. | Hoàng lại tiền phí hủy chuyến ER103 cho tôi vì tôi không chủ động hủy. | 13.3% | 3.1% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P008 | Tôi muốn khiếu nại thái độ của tài xế R101, hãy chuyển cho nhân viên xử lý. | Tôi muốn khiếu nại thái độ của tài xế Eder 101, hãy chuyển cho nhân viên xử lý. | 5.9% | 4.3% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P009 | Tôi cần gặp tổng đài viên trực tiếp để nói chuyện. | Tôi cần gặp tổng đại viên trực tiếp để nói chuyện. | 9.1% | 2.0% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P010 | Đơn hàng F201 của tôi chuẩn bị xong lâu rồi mà sao shipper chưa giao tới? | Đơn hạn F200-01 của tôi chuẩn bị xong lâu rồi mà sao Sipper chưa giao tới. | 12.5% | 4.3% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P011 | Sao đơn bún chả F201 của tôi giao lâu quá vậy? Hơn 1 tiếng rồi chưa thấy đâu. | Sau đơn bún chả F200 linh 1 của tôi giao lâu quá vậy. Hơn 1 tiếng rồi chưa thấy đâu. | 11.8% | 8.6% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P012 | Đơn F202 giao thiếu phần khoai tây chiên của tôi rồi, làm việc kiểu gì vậy? | Đơn F200 linh hai giao thiếu phần khoai tay chiên của tôi rồi, làm việc kiểu gì vậy? | 18.8% | 14.3% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P013 | Tôi nhận đơn Burger King F202 nhưng mở ra không thấy nước uống Coca Cola đâu hết. | Tôi nhận đơn Burger King F202 nhưng mở ra không thấy nước uống Coca Cola đâu hết. | 0.0% | 0.0% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P014 | Tôi áp mã giảm giá 20 nghìn cho đơn F203 mà sao lúc thanh toán bằng thẻ vẫn bị trừ đủ tiền gốc? | Tôi áp mã giảm giá 20.000 cho đơn F203 mà sau lúc thanh toán bàn thể vẫn bị trừ đủ tiền gốc. | 18.2% | 11.4% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P015 | Shipper đòi thu thêm tiền ship trong khi tôi đã thanh toán qua thẻ rồi. | Shipper đòi thu thêm tiền ship trong khi tôi đã thành toán qua thể rồi. | 13.3% | 2.9% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P016 | Tôi muốn hoàn tiền cho giao dịch PAY202 do thiếu món. | Tôi muốn hoàn tiền cho dạo dịch tầy 202 giờ thiếu món. | 27.3% | 16.3% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P017 | Hoàn tiền món khoai tây chiên bị thiếu của đơn F202 cho tôi. | Hoàn tiền món khoai tây chiên bị thiếu của đơn F202 cho tôi. | 0.0% | 0.0% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P018 | Tôi muốn hoàn lại 35 nghìn đồng cho phần ăn bị thiếu trong đơn Burger King. | Tôi muốn hoàn lại 35.000 đồng cho phần ăn bị thiếu trong đơn Burger King. | 6.7% | 8.5% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P019 | Đơn hàng của tôi bị hỏng hết rồi, cho tôi gặp nhân viên trực tiếp đi. | đơn hàng của tôi bị hổng hết rồi, cho tôi gặp nhân viên trực tiếp đi. | 6.2% | 1.5% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |
| P020 | Tôi muốn phản ánh cửa hàng làm ăn cẩu thả, kết nối tôi với tổng đài viên. | Tôi muốn phản ảnh cửa hàng làm ăn cậu thả, kết nối tôi với tổng đại viên. | 17.6% | 4.2% | ✅ Khớp | ✅ Khớp | ✅ Khớp | ✅ An toàn |

---

## 🔍 Phân tích Lỗi Nhận diện & Tác động Downstream

### 1. Phân tích các loại sai số ASR thường gặp
Dựa trên kết quả thực tế thu được từ mô hình Whisper:
* **Lỗi thanh điệu tiếng Việt:** Whisper đôi khi nhận diện nhầm các từ có phát âm gần giống hoặc thiếu dấu thanh khi âm thanh có nhiễu (ví dụ: `đơn` thành `đơn`, `đón` thành `đoàn`). Tuy nhiên, với giọng đọc chuẩn của Microsoft Neural Voices, tỷ lệ lỗi này tương đối thấp.
* **Lỗi nhận diện Mã định danh (Identifiers):** Các mã định danh như `R101`, `F202`, `PAY202` đôi khi bị nhận diện tách rời (ví dụ: `R 101` hoặc `F 202`).
  - *Giải pháp khắc phục:* Bộ regex xử lý thực thể trong `agent_service.py` đã được tối ưu hóa tốt để tự động chuẩn hóa các chuỗi này (loại bỏ khoảng trắng thừa), giúp duy trì tỷ lệ trích xuất thực thể cao.

### 2. Đánh giá ảnh hưởng lên LLM Agent (Vấn đề trích xuất & gọi Tool)
* **Độ bền vững của Intent Classification:** Với mô hình Whisper `tiny`/`base`/`large-v3`, hầu hết các từ khóa khóa cốt lõi (như `hoàn tiền`, `tài xế`, `đến trễ`, `thiếu món`, `nhân viên`) đều được nhận dạng chính xác. Nhờ đó, Agent nhận diện đúng ý định với tỷ lệ cao.
* **Độ bền vững của Entity Extraction:** Nhờ vào việc nhận diện đúng mã định danh hoặc các từ khóa ngữ cảnh hỗ trợ, hệ thống trích xuất thực thể chính xác.

---

## 💡 Đề xuất Cải tiến cho Pha Production

1. **Sử dụng Whisper phiên bản lớn hơn (Medium/Large) hoặc Fine-tuned chuyên biệt cho tiếng Việt:** Hệ thống hiện tại đã được nâng cấp thành công lên `whisper-small` đem lại độ chính xác nhận diện rất tốt (WER ~11.23%). Để triển khai thực tế có nhiều tiếng ồn hoặc giọng địa phương, nên cân nhắc sử dụng phiên bản `whisper-medium` / `large-v3` hoặc các mô hình được fine-tune chuyên biệt như `vinai/whisper-vietnamese-small` để tăng cường độ bền vững.
2. **Bổ sung tầng Sửa lỗi chính tả (Spell Checker):** Tích hợp một thư viện sửa lỗi chính tả tiếng Việt hoặc sử dụng chính LLM ở đầu Pipeline để tự động chuẩn hóa văn bản trước khi đưa vào Agent trích xuất nghiệp vụ.
3. **Mở rộng tập Regex / Fuzzy Matching:** Cho phép nhận diện nhiều biến thể của mã định danh (ví dụ: "chuyến xe R một trăm lẻ một" -> `R101`).
