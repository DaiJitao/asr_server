from fastapi import APIRouter, UploadFile, File, status
from app.schemas import ASRResponse, ASRData, HealthResponse
from app.services import asr_service
from app.core.logger import log

router = APIRouter()


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

        audio_data = await file.read()

        if not audio_data:
            return ASRResponse(
                code=1001,
                msg="音频文件为空",
                data=None
            )

        request_id, text, confidence, detected_lang, duration, processing_time = \
            await asr_service.transcribe_audio(
                audio_data,
                language=language,
                sample_rate=sample_rate,
                channels=channels
            )

        asr_data = ASRData(
            request_id=request_id,
            text=text,
            confidence=confidence,
            language=detected_lang,
            duration=duration,
            processing_time=processing_time
        )

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