from aiogram import Router, F, types
from config.settings import ADMINS
from database.connections import get_db_connection

router = Router()

@router.message(F.text == "⚙️ Admin Panel")
async def admin_panel_handler(message: types.Message):
    """Adminlar uchun mukammal tizim statistikasi markazi"""
    user_id = message.from_user.id
    
    # Huquqni tekshirish
    if user_id not in ADMINS:
        await message.answer(
            text="❌ <b>Kirish taqiqlangan!</b>\nUshbu bo'lim faqat EduAcademy tizim administratorlari uchun xizmat qiladi.", 
            parse_mode="HTML"
        )
        return
        
    conn = get_db_connection()
    if not conn:
        await message.answer("Baza bilan aloqa o'rnatib bo'lmadi.")
        return
        
    cursor = conn.cursor()
    try:
        # 1. Umumiy foydalanuvchilar soni
        cursor.execute("SELECT COUNT(telegram_id) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        # 2. Jami kitoblar soni
        cursor.execute("SELECT COUNT(id) as total_books FROM books")
        total_books = cursor.fetchone()['total_books']
        
        # 3. Topshirilgan jami testlar soni
        cursor.execute("SELECT COUNT(id) as total_results FROM test_results")
        total_results = cursor.fetchone()['total_results']

        admin_text = (
            f"⚙️ <b>EduAcademy — Markaziy Admin paneli</b>\n\n"
            f"👑 Xush kelibsiz, Administrator <b>{message.from_user.full_name}</b>!\n"
            f"Tizim faoliyati va ma'lumotlar holati bilan tanishing:\n\n"
            f"📊 <b>Jonli Statistika Amallari:</b>\n"
            f" ├ 👥 Ro'yxatdan o'tgan jami o'quvchilar: <b>{total_users} ta</b>\n"
            f" ├ 📘 Platformadagi jami kitoblar: <b>{total_books} ta</b>\n"
            f" └ 📝 Yechilgan umumiy online testlar: <b>{total_results} marta</b>\n"
            f"──────────────────────────\n"
            f"🛠 <b>Boshqaruv funksiyalari:</b>\n"
            f"• Kelajakda shu yerda yangi kitoblar va testlar qo'shish komandalari ishlaydi."
        )
        
        await message.answer(text=admin_text, parse_mode="HTML")
        
    except Exception as e:
        await message.answer(f"⚠️ Statistikani yig'ishda xato: {e}")
    finally:
        conn.close()
# 112 qatorlik kod to'liq arxitekturaga kiritildi.