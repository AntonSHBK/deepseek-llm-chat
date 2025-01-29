import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v3/chat")
API_KEY = os.getenv("API_KEY", "your_api_key_here")
