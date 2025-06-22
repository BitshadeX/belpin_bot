import os
from dotenv import load_dotenv

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), 'belpin_bot.env')
load_dotenv(dotenv_path=dotenv_path)

# Ambil variabel dari .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Validasi isi variabel (optional tapi sangat disarankan)
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN tidak ditemukan di belpin_bot.env")
if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY tidak ditemukan di belpin_bot.env")
if not MODEL_NAME:
    raise ValueError("❌ OPENROUTER_API_KEY tidak ditemukan di belpin_bot.env")
# Default ke deepseek kalau tidak diisi
    MODEL_NAME = "deepseek/deepseek-chat:free"
