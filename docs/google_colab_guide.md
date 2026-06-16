# Hướng dẫn Chạy Dự án trên Google Colab (GPU)

Tài liệu này hướng dẫn chi tiết cách chạy dự án **Voice Chatbot Agent** trên môi trường Google Colab để tận dụng GPU miễn phí (như Tesla T4), phục vụ cho việc nhận diện giọng nói bằng mô hình Whisper thời gian thực với độ trễ tối thiểu.

---

## Bước 1: Khởi tạo Notebook với GPU T4

1. Truy cập [Google Colab](https://colab.research.google.com/).
2. Chọn **File -> New notebook** để tạo notebook mới.
3. Kích hoạt GPU:
   * Trên thanh thực đơn, chọn **Edit -> Notebook settings** (hoặc **Runtime -> Change runtime type**).
   * Tại mục **Hardware accelerator**, chọn **GPU** (loại GPU mặc định thường là **T4**).
   * Nhấp **Save**.

---

## Bước 2: Tải Dự án lên Colab

Có 2 cách để đưa mã nguồn lên Colab:

### Cách A: Clone từ Git Repository (Khuyên dùng)
Chạy lệnh sau trong một cell trên Colab để tải mã nguồn:
```bash
!git clone <URL_REPOSITORY_CUA_BAN>
%cd voice-chatbot-agent
```

### Cách B: Upload file ZIP từ Máy tính
1. Nén thư mục dự án của bạn thành file `voice-chatbot-agent.zip`.
2. Trên bảng điều khiển bên trái của Colab, chọn biểu tượng **Files** (Thư mục) và click vào icon **Upload to session storage** để upload file zip lên.
3. Giải nén và chuyển thư mục:
```bash
!unzip voice-chatbot-agent.zip
%cd voice-chatbot-agent
```

---

## Bước 2.5: Cấu hình API Key & Biến môi trường (Colab Secrets)

Để sử dụng mô hình LLM Gemini thật sự thay vì cơ chế dự phòng bằng Regex, bạn cần cấu hình API Key thông qua tính năng **Secrets (Khóa bí mật)** trên Colab:
1. Nhấp vào biểu tượng chiếc chìa khóa **Secrets** ở thanh công cụ bên trái của Google Colab.
2. Thêm một khóa mới tên là `GEMINI_API_KEY` và dán API Key của bạn vào phần Value.
3. Bật quyền truy cập **Notebook access** cho khóa này.
4. Tạo một cell mới trong Colab và chạy đoạn code Python dưới đây để nạp khóa bí mật vào môi trường hệ thống:
```python
import os
from google.colab import userdata
try:
    os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")
    print("[+] Đã nạp khóa API Gemini thành công!")
except Exception as e:
    print(f"[-] Lỗi nạp khóa API: {e}. Hệ thống sẽ sử dụng Regex fallback.")
```

---

## Bước 3: Cài đặt Môi trường & Dependencies

Dự án đã đóng gói sẵn tập lệnh tự động hóa `colab_run.py` để giúp cài đặt `uv` và toàn bộ các thư viện nghiệp vụ chỉ với một dòng lệnh duy nhất:
```bash
!python colab_run.py --install
```
*Tập lệnh này sẽ cài đặt trình quản lý `uv`, đồng bộ các thư viện từ `pyproject.toml` (bao gồm `torch`, `openai-whisper`, `jiwer`, `soundfile`, `librosa`, `edge-tts`) trực tiếp vào hệ thống Python của Colab.*

---

## Bước 4: Chạy Đánh giá Chất lượng ASR (WER/CER/Latency)

Sử dụng GPU của Colab để nhận dạng giọng nói trên 20 file âm thanh mẫu và tính toán chỉ số lỗi.

### Chạy mô hình Whisper `small` (Tối ưu nhất về độ chính xác và tốc độ, mặc định):
```bash
!python colab_run.py --evaluate
```

### Chạy mô hình Whisper `base` (Nhẹ hơn, độ chính xác khá):
```bash
!python colab_run.py --eval-base
```

### Chạy mô hình Whisper `large-v3` (Mô hình lớn nhất, độ chính xác cao nhất, cần GPU VRAM lớn):
```bash
!python colab_run.py --eval-large
```
*Sau khi chạy xong, báo cáo chi tiết WER/CER và thời gian trễ của từng file sẽ được ghi trực tiếp vào tệp tin [docs/asr_evaluation_report.md](file:///c:/Users/Administrator/Developer/Intern_VSF/voice-chatbot-agent/docs/asr_evaluation_report.md).*

---

## Bước 5: Chạy các Bài Kiểm thử tự động (Pytest)

Để đảm bảo toàn bộ logic database và nghiệp vụ API hoạt động trơn tru:
```bash
!python colab_run.py --test
```

---

## Bước 6: Khởi chạy và Expose API Server ra ngoài Internet

Bạn có thể chạy server backend FastAPI trên Colab và mở cổng kết nối (tunneling) để ứng dụng khác gọi thử nghiệm.

### 1. Khởi chạy Server
Tạo một cell mới và khởi chạy tiến trình nền (server.log sẽ ghi log hoạt động):
```bash
!python colab_run.py --server > server.log 2>&1 &
```

### 2. Mở cổng kết nối bằng Localtunnel
Tạo một cell mới song song để mở kết nối public thông qua Localtunnel (miễn phí và không cần tạo tài khoản/token):
```bash
# Cài đặt localtunnel qua npm
!npm install -g localtunnel

# Expose cổng 8000 ra ngoài
!lt --port 8000
```
*Colab sẽ trả về một đường link dạng `https://XXXX.loca.lt`. Bạn có thể dùng đường link này làm Base URL để thực hiện gửi file âm thanh `/api/v1/chatbot/voice` từ Postman, cURL hoặc ứng dụng Frontend bên ngoài.*
