import time
import uuid
from typing import Optional, Tuple
import whisper
import os

from app.core.logger import log
from app.core.config import settings

class ASRService:
    def __init__(self, model_size: str = "medium"):
        log.info("ASR Service initialized")
        self.model_size = model_size
        self.model = whisper.load_model(model_size)
        self.model_dir = settings.ASR_model_dir

    async def transcribe_audio(
        self,
        audio_data: bytes,
        language: str = "zh",
        sample_rate: int = 16000,
        channels: int = 1
    ) -> Tuple[str, float, str, float]:
        request_id = str(uuid.uuid4())
        start_time = time.time()

        log.info(f"Processing transcription request {request_id}")

        try:
            duration = self._estimate_audio_duration(audio_data, sample_rate, channels)

            text = self._mock_transcription(language)
            confidence = 0.95

            processing_time = time.time() - start_time

            log.info(f"Transcription {request_id} completed in {processing_time:.2f}s")

            return request_id, text, confidence, language, duration, processing_time

        except Exception as e:
            log.error(f"Transcription {request_id} failed: {str(e)}")
            raise

    def _estimate_audio_duration(self, audio_data: bytes, sample_rate: int, channels: int) -> float:
        bytes_per_sample = 2
        total_samples = len(audio_data) // bytes_per_sample
        duration = total_samples / (sample_rate * channels)
        return max(duration, 0.1)

    def _mock_transcription(self, language: str) -> str:
        if language == "zh":
            return "这是一个语音识别服务的示例输出。"
        elif language == "en":
            return "This is a sample output from the speech recognition service."
        else:
            return "Unsupported language, defaulting to Chinese transcription."

    async def health_check(self) -> Tuple[str, str]:
        from app.core.config import settings
        return "healthy", settings.APP_VERSION

    async def speech_to_text(self, audio_path, model_size="medium"):
        """
        语音转文字核心函数
        :param audio_path: 音频文件路径（如./test.mp3）
        :param model_size: 模型大小（tiny/base/small/medium/large）
        :return: 识别后的文本
        """
        # 1. 检查音频文件是否存在
        if not os.path.exists(audio_path):
            log.error(f"音频文件不存在：{audio_path}")
            raise FileNotFoundError(f"音频文件不存在：{audio_path}")

        # 2. 加载Whisper模型（首次运行会自动下载模型文件，约几百MB~6GB）
        # model_size="base"：基础模型，适合CPU，中英文准确率不错
        # model_size="large"：大模型，准确率最高，建议GPU运行
        if model_size != self.model_size:
            self.model = whisper.load_model(model_size, download_root = self.model_dir)
            self.model_size = model_size

        # 3. 识别音频（自动处理音频采样率、格式转换等）
        result = self.model.transcribe(
            audio_path,
            language="zh",  # 指定语言为中文（可选："en"英文，不指定则自动检测）
            verbose=False,  # 关闭详细日志
            fp16=False      # CPU运行设为False，GPU设为True
        )
        # 4. 返回识别结果
        return result["text"]


asr_service = ASRService()



# 主函数：测试示例
async def test_speech_to_text():
    log.info("ASR Service standalone mode")
    # 替换为你的音频文件路径
    AUDIO_FILE = "/mlx/users/daijitao/asr_server/tests/data/2222.m4a"

    try:
        # 调用语音转文字
        text = await asr_service.speech_to_text(AUDIO_FILE, model_size="small")
        print("="*50)
        print("识别结果：")
        print(text)
        print("="*50)
    except Exception as e:
        print(f"识别失败：{e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_speech_to_text())