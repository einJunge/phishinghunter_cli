from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
TARGET_DOMAIN = os.getenv("TARGET_DOMAIN")

if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, VIRUSTOTAL_API_KEY, TARGET_DOMAIN]):
    raise ValueError("❌ Error: Una o más variables del archivo .env no están definidas.")

# Activa o desactiva el modo de simulación
DEMO_MODE = False

