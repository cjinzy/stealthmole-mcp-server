import os

import dotenv
from pydantic import BaseModel

dotenv.load_dotenv()


class StealthMoleConfig(BaseModel):
    access_key: str = os.getenv("STEALTHMOLE_ACCESS_KEY", "")
    secret_key: str = os.getenv("STEALTHMOLE_SECRET_KEY", "")
    base_url: str = "https://api.stealthmole.com"
    timeout: float = 600.0
    download_timeout: float = 600.0
    max_retries: int = 3
    retry_delay: float = 1.0
