class Settings:
    APP_NAME: str = "ASR Service"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8996

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"


settings = Settings()