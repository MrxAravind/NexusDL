from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.environ.get('API_ID', ''))
API_HASH = os.environ.get('API_HASH', '')
DATABASE_URL = os.getenv("DATABASE_URL")
DUMP_ID = int(os.environ.get('DUMP_CHAT_ID', ''))
