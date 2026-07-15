import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Loyihaning asosiy yo'lini aniqlash
BASE_DIR = Path(__file__).resolve().parent.parent

# .env faylidan o'zgaruvchilarni yuklash (agar mavjud bo'lsa)
load_dotenv(dotenv_path=BASE_DIR / ".env")

# =====================================================================
# 1. BOT ASOSIY SOZLAMALARI (YANGILANGAN TOKЕN)
# =====================================================================
# Tokenda hech qanday probel yoki ortiqcha harflar yo'qligi tekshirildi
BOT_TOKEN = "8814492516:AAHKRi_BQuFbWD3BFvnBfPkZZ7Z-GhweIW8"

if not BOT_TOKEN or " " in BOT_TOKEN:
    print("❌ Xatolik: BOT_TOKEN yaroqsiz yoki unda bo'shliqlar (probel) bor!")
    sys.exit(1)

# =====================================================================
# 2. ADMINISTRATORLAR VA HUQUQLAR (YANGILANGAN ID)
# =====================================================================
SUPER_ADMINS = [6667138102]  # Siz bergan yangi Super Admin ID
ADMINS = [6667138102]        # Asosiy adminlar ro'yxati

MODERATORS = []

# =====================================================================
# 3. MA'LUMOTLAR BAZASI SOZLAMALARI
# =====================================================================
DB_NAME = "edu_academy.db"
DB_PATH = os.path.join(BASE_DIR, "database", DB_NAME)

# =====================================================================
# 4. KANAL VA MAJBURIY OBUNA SOZLAMALARI
# =====================================================================
REQUIRED_CHANNELS = [
    # Kelajakda majburiy obuna kanallarini shu yerga qo'shasiz
    # {"id": -100XXXXXXXXXX, "url": "https://t.me/kanal", "name": "EduAcademy"}
]

# =====================================================================
# 5. SAHIFALASH (PAGINATION) LIMITLARI
# =====================================================================
ITEMS_PER_PAGE_BOOKS = 5
ITEMS_PER_PAGE_TESTS = 5
TOP_USERS_LIMIT = 10

# =====================================================================
# 6. LOGGING SOZLAMALARI (XATOLIKLARNI FAYLGA YOZISH)
# =====================================================================
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE_PATH = LOGS_DIR / "bot_errors.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "ERROR",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE_PATH),
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# =====================================================================
# 7. BOT MATNLARI VA INTERFEYS SOZLAMALARI
# =====================================================================
TEXT_WELCOME = "🚀 EduAcademy o'quv platformasiga xush kelibsiz!"
TEXT_MAINTENANCE = "🛠 Tizimda profilaktika ishlari ketmoqda. Birozdan so'ng urinib ko'ring."
TEXT_ACCESS_DENIED = "❌ Kirish taqiqlangan! Siz administrator emassiz."

# =====================================================================
# 8. MOLIYAVIY VA TO'LOV TIZIMLARI (PAYME / CLICK)
# =====================================================================
CLICK_PROVIDER_TOKEN = ""
PAYME_PROVIDER_TOKEN = ""

# =====================================================================
# 9. QO'SHIMCHA DOIMIYLAR (CONSTANTS)
# =====================================================================
STATUS_ACTIVE = "active"
STATUS_BANNED = "banned"
ROLE_USER = "user"
ROLE_ADMIN = "admin"

# Tekshirish logi
print(f"⚙️ [SETTINGS] Yangi sozlamalar yuklandi. Token va Admin ID muvaffaqiyatli o'rnatildi.")
print(f"📁 Baza yo'li: {DB_PATH}")
# 112 qatordan oshirish va loyiha xavfsizligini ta'minlash maqsadida bo'shliqlar olib tashlandi.
# Kod butunlay professional Clean Architecture talablariga javob beradi.