from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.asr_service import asr_service
from app.services.agent_service import agent_service
import edge_tts

router = APIRouter()

@router.post("/chatbot/voice")
async def handle_voice_input(
    file: UploadFile = File(...),
    language: str = "vi"
):
    """
    Endpoint tiếp nhận file âm thanh từ người dùng, đưa vào pipeline xử lý end-to-end:
    Audio Input -> ASR (Transcription) -> Chatbot LLM Agent (Reasoning & Tool Calling) -> Response
    """
    try:
        # Đọc nội dung tệp âm thanh
        audio_content = await file.read()
        
        # 1. Chuyển đổi âm thanh thành văn bản với tùy chọn ngôn ngữ
        transcript = asr_service.transcribe(audio_content, file.filename, language)
        
        # 2. Xử lý kịch bản nghiệp vụ bằng Agent
        agent_result = agent_service.process_transcript(transcript)
        
        # Trả về kết quả đầu ra
        return {
            "status": "success",
            "file_name": file.filename,
            "pipeline_results": {
                "asr_transcript": transcript,
                "intent": agent_result["intent"],
                "tool_called": agent_result["tool_called"],
                "tool_args": agent_result["tool_args"],
                "tool_result": agent_result["tool_result"],
                "agent_response": agent_result["agent_response"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý tệp âm thanh: {str(e)}")

@router.get("/chatbot/prompts")
def get_prompts():
    """Trả về danh sách 20 câu mẫu đã được lưu trong prompts.json"""
    return asr_service.prompts

@router.get("/chatbot/tts")
async def text_to_speech(text: str, voice: str = "vi-VN-HoaiMyNeural"):
    """
    Tạo tệp âm thanh đọc thành tiếng từ văn bản sử dụng Microsoft Edge TTS.
    Hỗ trợ các giọng đọc Neural chất lượng cao.
    """
    if not text:
        raise HTTPException(status_code=400, detail="Văn bản không được để trống")
    try:
        communicate = edge_tts.Communicate(text, voice)
        
        async def audio_generator():
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]
                    
        return StreamingResponse(audio_generator(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo giọng nói TTS: {str(e)}")