from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 720  # 30 days

    # Reset tokens
    RESET_TOKEN_EXPIRY_MINUTES: int = 30

    # Auth rate limiting (per IP, per action)
    AUTH_RATE_LIMIT_MAX: int = 5
    AUTH_RATE_LIMIT_WINDOW_MINUTES: int = 15

    # App base URL (used for reset email links, magic links, QR codes)
    APP_URL: str = "http://localhost:3000"

    # Static files base URL (used for image URLs)
    # This should be the public URL of the API server (e.g. http://localhost:8000)
    STATIC_FILES_BASE_URL: str = "http://localhost:8000"

    # Local storage for uploads
    UPLOADS_DIR: str = "uploads"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
