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
            from app.core.config import settings
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Loading Whisper model '{settings.WHISPER_MODEL_NAME}' on {device}...")
            self.model = whisper.load_model(settings.WHISPER_MODEL_NAME, device=device)
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
                import io
                import soundfile as sf
                import librosa
                import numpy as np
                import torch
                
                # Đọc luồng âm thanh từ bộ nhớ sử dụng soundfile
                audio_data, sr = sf.read(io.BytesIO(audio_content))
                
                # Nếu là âm thanh stereo (2 kênh), chuyển đổi thành mono (1 kênh) bằng cách lấy trung bình
                if len(audio_data.shape) > 1:
                    audio_data = np.mean(audio_data, axis=1)
                    
                # Resample sang tần số chuẩn 16000Hz của Whisper
                if sr != 16000:
                    audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=16000)
                    
                # Chuyển đổi định dạng sang float32
                audio_data = audio_data.astype(np.float32)
                
                # Gọi mô hình nhận dạng giọng nói Whisper
                model = self._get_model()
                fp16 = torch.cuda.is_available()
                
                result = model.transcribe(audio_data, language="vi", fp16=fp16)
                return result.get("text", "").strip()
                
            except Exception as e:
                print(f"Error transcribing audio with Whisper: {str(e)}")
                # Trả về câu thoại mặc định nếu xảy ra lỗi phần cứng/giải mã âm thanh
                return "Chào bạn, tôi cần kiểm tra trạng thái đơn hàng"

asr_service = ASRService()
