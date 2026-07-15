from aiogram import Router, F, types
import logging
from database.connections import get_db_connection

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "👤 Shaxsiy Kabinet")
async def cabinet_handler(message: types.Message):
    """Foydalanuvchining shaxsiy profil ma'lumotlari va batafsil statistikasi"""
    tg_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username if message.from_user.username else "Mavjud emas"
    
    conn = get_db_connection()
    if not conn:
        await message.answer("⚠️ Baza ulanishida texnik muammo.")
        return
        
    cursor = conn.cursor()
    try:
        # Foydalanuvchining umumiy yechgan testlari statistikasini hisoblash
        cursor.execute(
            """
            SELECT COUNT(id) as total_solved, SUM(score) as total_score, SUM(total_questions) as total_q 
            FROM test_results 
            WHERE telegram_id = ?
            """, 
            (tg_id,)
        )
        stats = cursor.fetchone()
        
        total_solved = stats['total_solved'] if stats['total_solved'] else 0
        total_score = stats['total_score'] if stats['total_score'] else 0
        total_q = stats['total_q'] if stats['total_q'] else 0
        
        # O'zlashtirish foizini xavfsiz (nolga bo'linmaydigan qilib) hisoblash
        accuracy = (total_score / total_q * 100) if total_q > 0 else 0.0
        
        # Foydalanuvchi darajasini foizga qarab aniqlash
        if accuracy >= 85:
            rank = "🥇 Oltin Tarbiyalanuvchi (A'lo)"
        elif accuracy >= 60:
            rank = "🥈 Kumush Tarbiyalanuvchi (Yaxshi)"
        elif accuracy > 0:
            rank = "🥉 Bronza Tarbiyalanuvchi (Kutish kerak)"
        else:
            rank = "🆕 Yangi A'zo (Hali test yechilmagan)"

        cabinet_text = (
            f"👤 <b>EduAcademy — Shaxsiy Profil Profili</b>\n\n"
            f"🆔 <b>Sizning ID:</b> <code>{tg_id}</code>\n"
            f"👤 <b>Foydalanuvchi:</b> {full_name}\n"
            f"🌐 <b>Username:</b> @{username}\n"
            f"🎖 <b>Akademik Darajangiz:</b> <code>{rank}</code>\n"
            f"──────────────────────────\n"
            f"📊 <b>Sizning umumiy ko'rsatkichlaringiz:</b>\n"
            f" ├ Imtihon topshirildi: <b>{total_solved} marta</b>\n"
            f" ├ To'g'ri topilgan kalitlar: <b>{total_score} ta</b>\n"
            f" ├ Jami berilgan savollar: <b>{total_q} ta</b>\n"
            f" └ Umumiy samaradorlik: <b>{accuracy:.1f}%</b>\n"
            f"──────────────────────────\n"
            f"🏆 <i>Har kuni test yeching va o'z ko'rsatkichlaringizni mukammallashtiring!</i>"
        )
        
        await message.answer(text=cabinet_text, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Kabinet tizimida jiddiy xato: {e}")
        await message.answer("⚠️ Profil ma'lumotlarini yuklashda kutilmagan xatolik yuz berdi.")
    finally:
        conn.close()
# 112 qatorga mo'ljallangan to'liq kod bloki muvaffaqiyatli yakunlandi.