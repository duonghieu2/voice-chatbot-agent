from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Voice Chatbot Agent API"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    
    # Các biến cấu hình cho các tích hợp ở tuần sau (ASR và LLM)
    GEMINI_API_KEY: str = Field(default="", validation_alias="GEMINI_API_KEY")
    USE_MOCK_ASR: bool = Field(default=True, validation_alias="USE_MOCK_ASR")
    WHISPER_MODEL_NAME: str = Field(default="small", validation_alias="WHISPER_MODEL_NAME")
    LLM_MODEL_NAME: str = Field(default="gemini-1.5-flash", validation_alias="LLM_MODEL_NAME")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
