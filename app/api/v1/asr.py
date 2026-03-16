from fastapi import APIRouter, UploadFile, File, status
import os
import time
import uuid

from app.schemas import ASRResponse, ASRData, HealthResponse
from app.services import asr_service
from app.core.logger import log
from app.core.config import settings


router = APIRouter()


def save_audio_file(audio_data: bytes, audio_path: str):
    """保存音频文件到指定路径"""
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(audio_data)

def delete_audio_file(audio_path: str):
    """删除指定路径的音频文件"""
    if os.path.exists(audio_path):
        os.remove(audio_path)
        log.info(f"Deleted audio file: {audio_path}")
    else:
        log.warning(f"Audio file not found: {audio_path}")

@router.post(
    "/transcribe",
    response_model=ASRResponse,
    responses={
        200: {"model": ASRResponse},
    }
)
async def transcribe_audio(
    file: UploadFile = File(..., description="音频文件"),
    language: str = "zh",
    sample_rate: int = 16000,
    channels: int = 1
):
    try:
        log.info(f"Received transcription request for file: {file.filename}")

        # 第一步：接受音频文件
        audio_data = await file.read()
        
        if not audio_data:
            return ASRResponse(
                code=1001,
                msg="音频文件为空",
                data=None
            )
        
        # 第二步：保存音频文件到本地缓存目录
        request_id = str(uuid.uuid4())
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        audio_path = os.path.join(settings.audio_dir, f"{timestamp}_{file.filename}")
        
        save_audio_file(audio_data, audio_path)
        log.info(f"Audio file saved to: {audio_path}")
        
        # 第三步：进行语音识别
        text, processing_time = await asr_service.speech_to_text(audio_path)
        
        asr_data = ASRData(
            request_id=request_id,
            text=text,
            confidence=0.95,
            language=language,
            duration=0.0,
            processing_time=processing_time
        )
        delete_audio_file(audio_path)
        
        return ASRResponse(
            code=0,
            msg="语音识别成功",
            data=asr_data
        )
        
    except Exception as e:
        log.error(f"Transcription failed: {str(e)}")
        return ASRResponse(
            code=1000,
            msg=f"语音识别服务异常: {str(e)}",
            data=None
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    responses={200: {"model": HealthResponse}}
)
async def health_check():
    status_str, version = await asr_service.health_check()
    return HealthResponse(
        status=status_str,
        version=version
    )

    
