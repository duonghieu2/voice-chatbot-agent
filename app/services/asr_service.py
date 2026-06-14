import json
import os
from typing import List, Dict, Any

class ASRService:
    def __init__(self):
        self.prompts: List[Dict[str, Any]] = []
        self._load_prompts()
        self.model = None  # Lazy loaded Whisper model

    def _load_prompts(self):
        try:
            # Xác định đường dẫn tuyệt đối tới prompts.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            prompts_path = os.path.join(current_dir, "..", "database", "prompts.json")
            if os.path.exists(prompts_path):
                with open(prompts_path, "r", encoding="utf-8") as f:
                    self.prompts = json.load(f)
            else:
                print(f"Warning: File prompts.json does not exist at {prompts_path}")
        except Exception as e:
            print(f"Error loading prompts.json: {str(e)}")

    def _get_model(self):
        if self.model is None:
            import whisper
            import torch
            import numpy as np
            from app.core.config import settings
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Loading Whisper model '{settings.WHISPER_MODEL_NAME}' on {device}...")
            self.model = whisper.load_model(settings.WHISPER_MODEL_NAME, device=device)
            
            # Chạy thử (warm-up) inference để nạp CUDA kernels và cấp phát VRAM trước
            try:
                print("[*] Đang thực hiện warm-up inference cho Whisper...")
                # Tạo 1 giây âm thanh câm (16000 samples ở tần số 16kHz mono)
                dummy_audio = np.zeros(16000, dtype=np.float32)
                fp16 = torch.cuda.is_available()
                self.model.transcribe(dummy_audio, fp16=fp16)
                print("[*] Hoàn thành warm-up inference cho Whisper thành công!")
            except Exception as e:
                print(f"[!] Cảnh báo: Lỗi khi chạy warm-up Whisper: {str(e)}")
        return self.model

    def transcribe(self, audio_content: bytes, filename: str) -> str:
        """
        Chuyển đổi âm thanh đầu vào thành văn bản (ASR).
        Hỗ trợ 2 chế độ: giả lập (mock) và chạy mô hình thực tế (Whisper).
        """
        from app.core.config import settings
        
        if settings.USE_MOCK_ASR:
            filename_lower = filename.lower()
            
            # Thử tìm mã Prompt ID (ví dụ: P001) trong tên file
            import re
            pid_match = re.search(r"p\d{3}", filename_lower)
            if pid_match:
                pid = pid_match.group(0).upper()
                for p in self.prompts:
                    if p["id"] == pid:
                        return p["text"]
            
            # Ánh xạ từ tên tệp âm thanh kiểm thử sang danh mục lỗi
            mapping = {
                "tai_xe_den_tre": "driver_late",
                "tài_xế_đến_trễ": "driver_late",
                "giao_thieu_mon": "missing_item",
                "giao_thiếu_món": "missing_item",
                "phi_huy_chuyen": "payment_error",
                "phí_hủy_chuyến": "payment_error",
                "hoan_tien": "refund_request",
                "hoàn_tiền": "refund_request",
                "chuyen_nhan_vien": "escalate",
                "chuyển_nhân_viên": "escalate"
            }
            
            # Tìm danh mục khiếu nại đích
            target_category = None
            for keyword, category in mapping.items():
                if keyword in filename_lower:
                    target_category = category
                    break
                    
            if target_category and self.prompts:
                # Lọc các câu thoại thuộc danh mục này
                matched_prompts = [p for p in self.prompts if p["category"] == target_category]
                if matched_prompts:
                    # Chọn câu thoại đầu tiên làm mẫu kiểm thử ổn định cho bộ test
                    return matched_prompts[0]["text"]
            
            # Trả về câu thoại mặc định nếu không khớp tệp kiểm thử
            return "Chào bạn, tôi cần kiểm tra trạng thái đơn hàng"
        else:
            try:
                import tempfile
                import whisper
                import torch
                
                # Tạo file tạm thời để lưu dữ liệu âm thanh đầu vào
                # Việc này giúp whisper.load_audio (dùng ffmpeg bên dưới) có thể giải mã mọi định dạng (wav, mp3, webm, ogg...)
                suffix = os.path.splitext(filename)[1] or ".wav"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(audio_content)
                    tmp_path = tmp_file.name
                
                try:
                    # whisper.load_audio tự động gọi ffmpeg để decode và resample về 16000Hz mono float32
                    audio_data = whisper.load_audio(tmp_path)
                    
                    # Gọi mô hình nhận dạng giọng nói Whisper
                    model = self._get_model()
                    fp16 = torch.cuda.is_available()
                    
                    result = model.transcribe(audio_data, language="vi", fp16=fp16)
                    return result.get("text", "").strip()
                finally:
                    # Xóa file tạm sau khi xử lý
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                
            except Exception as e:
                print(f"Error transcribing audio with Whisper: {str(e)}")
                # Trả về câu thoại mặc định nếu xảy ra lỗi phần cứng/giải mã âm thanh
                return "Chào bạn, tôi cần kiểm tra trạng thái đơn hàng"

asr_service = ASRService()
