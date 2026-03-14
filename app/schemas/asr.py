from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ASRRequest(BaseModel):
    language: Optional[str] = Field(default="zh", description="语言代码，如 zh, en")
    sample_rate: Optional[int] = Field(default=16000, description="采样率")
    channels: Optional[int] = Field(default=1, description="声道数")


class ASRData(BaseModel):
    request_id: str = Field(..., description="请求ID")
    text: str = Field(..., description="识别文本")
    confidence: float = Field(..., description="置信度")
    language: str = Field(..., description="识别的语言")
    duration: float = Field(..., description="音频时长(秒)")
    processing_time: float = Field(..., description="处理时长(秒)")


class ASRResponse(BaseModel):
    code: int = Field(..., description="响应码，0表示成功，其他表示失败")
    msg: str = Field(..., description="响应消息")
    data: Optional[ASRData] = Field(default=None, description="响应数据，成功时返回")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    status: str = Field(..., description="服务状态")
    version: str = Field(..., description="服务版本")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    error_code: str = Field(..., description="错误码")
    error_message: str = Field(..., description="错误信息")
    timestamp: datetime = Field(default_factory=datetime.utcnow)