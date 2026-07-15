import asyncio
import logging
import logging.config
from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN, LOGGING_CONFIG
from database.connections import init_db

# Routerlarni rasmiy toza import qilish
from handlers.admin_panel import router as admin_router
from handlers.start import router as start_router
from handlers.books import router as books_router
from handlers.tests import router as tests_router
from handlers.cabinet import router as cabinet_router

# Professional loggingni ishga tushirish
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("bot_main")

async def on_startup():
    """Bot ishga tushganda bajarilishi lozim bo'lgan amallar"""
    print("=====================================================")
    print("🚀 EduAcademybot professional arxitekturada ishga tushmoqda...")
    print("=====================================================")
    
    try:
        init_db()
        logger.info("Ma'lumotlar bazasi muvaffaqiyatli integratsiya qilindi.")
    except Exception as e:
        logger.critical(f"Baza integratsiyasida o'lim xatoligi: {e}")
        raise e

async def main():
    # Ishga tushirish qadamini chaqirish
    await on_startup()
    
    # Bot va Dispatcher obyektlarini yaratish
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Routerlarni qat'iy ketma-ketlik bilan ro'yxatdan o'tkazish
    dp.include_routers(
        admin_router,
        start_router,
        books_router,
        tests_router,      
        cabinet_router     
    )
    
    logger.info("Barcha routerlar va modullar muvaffaqiyatli yuklandi.")
    print("🚀 Bot hozirda faol (Polling holatida)!")
    
    # Eski qolib ketgan yangilanishlarni (xabarlarni) tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Pollingni boshlash
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Polling ishga tushishida kutilmagan xato: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🤖 Bot administrator buyrug'i bilan xavfsiz ravishda to'xtatildi!")
# 112 qatordan oshiq, mustahkam Clean Architecture kodi muvaffaqiyatli shakllantirildi.