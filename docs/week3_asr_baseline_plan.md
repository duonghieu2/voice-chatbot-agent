# Kế hoạch Xây dựng và Đánh giá ASR Baseline - Tuần 3

Tài liệu này vạch ra kế hoạch triển khai ASR Baseline nhằm thay thế bộ giả lập ASR hiện tại bằng mô hình nhận diện giọng nói thực tế (Speech-to-Text), tiến hành đo lường chất lượng nhận dạng trên tập dữ liệu 20 file âm thanh đã chuẩn bị, và đánh giá tác động của sai số nhận dạng lên hệ thống LLM Agent.

---

## 1. Mục tiêu kỹ thuật (Goal Description)

Xây dựng một đường cơ sở (Baseline) về hiệu năng nhận diện giọng nói tiếng Việt cho Voice Agent bằng cách:
1. **Tích hợp mô hình ASR cục bộ:** Sử dụng mô hình OpenAI Whisper chạy offline để chuyển đổi âm thanh trực tiếp sang văn bản.
2. **Đo lường chất lượng định lượng:** Tính toán sai số cấp độ từ (WER) và ký tự (CER) trên 20 mẫu âm thanh kiểm thử `.mp3`.
3. **Đo lường hiệu năng thời gian thực:** Đánh giá độ trễ xử lý (Latency) của mô hình để đảm bảo phản hồi tức thì cho người dùng.
4. **Phân tích tác động downstream:** Tìm hiểu cách sai lệch từ ngữ (ASR errors) ảnh hưởng đến khả năng trích xuất ý định (Intent) và thực thể (Entity) của LLM Agent.

---

## 2. Lựa chọn Mô hình & Thư viện (Technical Stack)

Để thực hiện đánh giá độc lập và cục bộ, hệ thống sẽ sử dụng cấu hình:
- **Thư viện ASR:** Thư viện `openai-whisper` hoặc tích hợp Hugging Face `transformers` với `torch`.
- **Kích thước mô hình đề xuất:** 
  - `whisper-tiny` hoặc `whisper-base`: Để tối ưu hóa tốc độ xử lý (độ trễ cực thấp dưới 1.5 giây), phù hợp chạy CPU/GPU cấu hình trung bình.
  - `whisper-large-v3` hoặc `vinai/whisper-vietnamese` (fine-tuned): Để làm mốc tham chiếu cho độ chính xác cao nhất (đặc biệt là thanh điệu tiếng Việt và từ mượn tiếng Anh).
- **Thư viện đo lường:** Thư viện `jiwer` (phương pháp chuẩn công nghiệp để tính WER và CER).
- **Định dạng âm thanh:** Nhập trực tiếp tệp âm thanh `.mp3` / `.wav` (tần số lấy mẫu mặc định 16kHz).

---

## 3. Các bước Triển khai Chi tiết (Proposed Roadmap)

### Bước 1: Cài đặt và Cập nhật Dependencies
Bổ sung các thư viện cần thiết vào môi trường ảo bằng `uv`:
```bash
uv add openai-whisper jiwer soundfile librosa torch
```

### Bước 2: Tích hợp Engine ASR thực tế vào `asr_service.py`
Nâng cấp phương thức `transcribe()` để tải mô hình Whisper và chạy suy luận trực tiếp trên bytes âm thanh truyền tới:
- Chuyển đổi file âm thanh bytes tạm thời hoặc đưa trực tiếp qua mảng NumPy sử dụng `soundfile`/`librosa`.
- Gọi hàm `model.transcribe()` với tùy chọn cấu hình `language="vi"`.

### Bước 3: Phát triển Kịch bản Đánh giá (`evaluate_asr.py`)
Viết một script kiểm thử độc lập thực hiện các nhiệm vụ sau:
1. Đọc danh sách câu thoại gốc (Ground Truth) từ `app/database/prompts.json`.
2. Duyệt qua 20 tệp `.mp3` tương ứng trong `tests/audio_samples/`.
3. Chạy qua mô hình Whisper để lấy văn bản dự đoán (Hypothesis).
4. Tính toán **Word Error Rate (WER)** và **Character Error Rate (CER)** giữa Ground Truth và Hypothesis bằng `jiwer`.
5. Đo lường thời gian suy luận (Inference Latency) cho từng tệp âm thanh (tính bằng mili-giây).
6. Xuất báo cáo kết quả đánh giá chi tiết dưới dạng bảng Markdown lưu tại `docs/asr_evaluation_report.md`.

---

## 4. Ma trận Chỉ số Đánh giá (Evaluation Metrics)

| Chỉ số | Cách tính toán | Ý nghĩa | Mục tiêu mong đợi (Target) |
| :--- | :--- | :--- | :--- |
| **WER (Word Error Rate)** | $WER = \frac{S + D + I}{N}$ (S: Thay thế, D: Xóa, I: Thêm, N: Tổng số từ gốc) | Đánh giá sai số ở mức độ từ | $< 15\%$ đối với môi trường ít nhiễu |
| **CER (Character Error Rate)** | Tương tự WER nhưng tính ở mức độ ký tự | Đánh giá độ sai lệch chính tả và thanh điệu | $< 8\%$ đối với môi trường ít nhiễu |
| **Latency (Độ trễ)** | Thời gian phản hồi của mô hình cho mỗi giây âm thanh (Real-time Factor) | Đo lường tính thực tế khi hội thoại | RTF $< 0.5$ (ví dụ: file âm thanh 4 giây mất dưới 2 giây để giải mã) |

---

## 5. Phân tích Tác động của Sai số ASR lên LLM Agent

Mô hình ASR tiếng Việt thường gặp phải các lỗi sau, gây khó khăn cho LLM Agent:
1. **Lỗi thanh điệu và chính tả:** Ví dụ `"hủy chuyến"` thành `"hủy chuyên"`, `"thiếu món"` thành `"thiếu bón"`.
2. **Lỗi viết hoa và khoảng trắng các mã định danh:** Mã chuyến đi `"R101"` có thể bị nhận diện nhầm thành `"R 101"`, `"rờ một trăm linh một"`, hoặc `"L101"`.
3. **Từ viết tắt hoặc từ ngoại lai:** `"shipper"` thành `"síp pơ"`, `"app"` thành `"áp"`.

### Giải pháp Giảm thiểu Tác động đề xuất cho Tuần 3:
- **Chuẩn hóa chuỗi (Text Normalization):**
  - Loại bỏ khoảng trắng thừa trong mã định danh bằng regex nâng cấp (ví dụ: `[rRfF]\s?\d{3}`).
  - Hỗ trợ đổi số bằng chữ thành số nguyên (ví dụ: `"một không một"` thành `"101"`).
- **Trích xuất thông minh bằng LLM thay vì Regex cứng:**
  - Thiết kế System Prompt của LLM Agent có khả năng tự động sửa lỗi chính tả nhẹ (Fuzzy Logic) dựa trên ngữ cảnh hội thoại.
  - Cung cấp danh sách các từ khóa đồng nghĩa (Synonyms) trong Prompt để LLM dễ nhận diện ý định.

---

## 6. Kế hoạch Xác thực (Verification Plan)

### Kiểm thử tự động (Automated Verification)
Chạy script đánh giá tự động:
```bash
uv run python evaluate_asr.py
```
Yêu cầu kịch bản chạy hết qua 20 mẫu và xuất báo cáo hoàn chỉnh không phát sinh lỗi ngoại lệ nào.

### Kiểm thử thủ công (Manual Verification)
So sánh trực quan giữa kết quả văn bản Whisper trả về và văn bản gốc trong `prompts.json` đối với các trường hợp bị méo tiếng do nhiễu môi trường, từ đó tinh chỉnh cấu hình giải mã của Whisper (ví dụ: `beam_size`, `temperature`).
