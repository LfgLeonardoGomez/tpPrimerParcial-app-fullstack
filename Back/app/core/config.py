
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
# ─── JWT ──────────────────────────────────────────────────────────────────
    SECRET_KEY: str                    # Obligatorio — sin default. Mínimo 32 chars.
    ALGORITHM:  str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = {
        "env_file":          ".env",
        "env_file_encoding": "utf-8",
        "extra":             "ignore",   # ignora vars extra del .env (ej. DATABASE_URL literal)
    }

# ___ CLOUDINARY _____

    cloudinary_cloud_name: str = ""
    cloudinary_api_key:    str = ""
    cloudinary_api_secret: str = ""
    
settings = Settings()