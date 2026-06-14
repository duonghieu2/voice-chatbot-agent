from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from app.routers import chatbot, tools
import os
from contextlib import asynccontextmanager

# 0. Thiết lập lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Tải trước (pre-warm) mô hình Whisper và Gemini LLM khi khởi động server"""
    from app.core.config import settings
    
    # 1. Tải trước và warm-up mô hình Whisper ASR (nếu tắt Mock)
    if not settings.USE_MOCK_ASR:
        print("[*] Đang tải trước mô hình Whisper ASR vào bộ nhớ khi khởi động server...")
        from app.services.asr_service import asr_service
        # Gọi load model (có tích hợp sẵn warm-up inference bên trong)
        asr_service._get_model()
        print("[*] Mô hình Whisper ASR đã được tải sẵn sàng!")
        
    # 2. Khởi tạo và cấu hình trước các mô hình Gemini LLM
    if settings.GEMINI_API_KEY:
        print("[*] Đang khởi tạo trước cấu hình Gemini LLM...")
        from app.services.agent_service import agent_service
        agent_service.initialize_models()
        print("[*] Mô hình Gemini LLM đã sẵn sàng!")
        
    yield

# 1. Khởi tạo ứng dụng FastAPI với lifespan
app = FastAPI(
    title="Voice Chatbot Agent API",
    description="Backend phục vụ pipeline Voice Chatbot đặt xe và đặt đồ ăn",
    version="0.1.0",
    lifespan=lifespan
)

# 2. Cấu hình CORS để đảm bảo Frontend có thể gọi API sau này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên giới hạn lại domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount thư mục static phục vụ giao diện HTML/CSS/JS
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 4. Đăng ký các router xử lý kịch bản chatbot và tools gọi dịch vụ mock
app.include_router(chatbot.router, prefix="/api/v1", tags=["Chatbot"])
app.include_router(tools.router, prefix="/api/v1", tags=["Tools"])
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    favicon_path = os.path.join(static_dir, "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return Response(status_code=204)

@app.get("/")
def read_root(request: Request):
    accept = request.headers.get("accept", "")
    # Nếu client yêu cầu JSON (ví dụ như bộ test client)
    if "text/html" not in accept:
        return {"message": "Voice Chatbot Agent API đang hoạt động ổn định!"}
    
    # Nếu client là trình duyệt yêu cầu HTML
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)