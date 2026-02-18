import os
from dotenv import load_dotenv

load_dotenv()

# .env dosyasında değişkenleri çeker
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
LOG_FILE = os.getenv("LOG_FILE")
MAX_LOG_SIZE_MB = int(os.getenv("MAX_LOG_SIZE_MB"))
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT"))
