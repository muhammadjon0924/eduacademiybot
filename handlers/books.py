from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
from database.connections import get_db_connection

router = Router()
logger = logging.getLogger(__name__)

def get_books_keyboard(books_list):
    """Kitoblar uchun inline tugmalarni yaratish"""
    builder = InlineKeyboardBuilder()
    for book in books_list:
        builder.row(types.InlineKeyboardButton(
            text=f"📘 {book['title']}", 
            callback_data=f"view_book_{book['id']}"
        ))
    return builder.as_markup()

@router.message(F.text == "📚 Kitoblar")
async def books_catalog_handler(message: types.Message):
    """Mavjud kitoblar katalogini inline tugmalar shaklida chiqarish"""
    conn = get_db_connection()
    if not conn:
        await message.answer("⚠️ Ma'lumotlar bazasiga ulanishda xato. Birozdan so'ng urinib ko'ring.")
        return
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, downloads_count FROM books ORDER BY id DESC")
        books = cursor.fetchall()
        
        if not books:
            await message.answer(
                "📚 <b>EduAcademy elektron kutubxonasi</b>\n\n"
                "Ayni paytda tizimga yangi kitoblar yuklanish jarayonida. Iltimos, keyinroq tekshirib ko'ring!",
                parse_mode="HTML"
            )
            return

        text = (
            "📚 <b>EduAcademy Elektron Kutubxonasi</b>\n\n"
            "Siz bu yerda o'zingizga kerakli bo'lgan o'quv qo'llanmalarini mutlaqo bepul yuklab olishingiz mumkin.\n\n"
            "👇 Yuklamoqchi bo'lgan kitobingiz ustiga bosing:"
        )
        
        await message.answer(
            text=text,
            parse_mode="HTML",
            reply_markup=get_books_keyboard(books)
        )
        
    except Exception as e:
        logger.error(f"Kitoblar ro'yxatida xato: {e}")
        await message.answer("⚠️ Tizimda kutilmagan xatolik yuz berdi.")
    finally:
        conn.close()

@router.callback_query(F.data.startswith("view_book_"))
async def view_book_callback(call: types.CallbackQuery):
    """Inline tugma bosilganda kitob tafsilotlarini ko'rsatish va faylni yuborish"""
    book_id = int(call.data.split("_")[2])
    
    conn = get_db_connection()
    if not conn:
        await call.answer("Baza bilan aloqa yo'q!", show_alert=True)
        return
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        
        if not book:
            await call.answer("Kitob topilmadi!", show_alert=True)
            return
            
        # Yuklashlar sonini oshirish
        cursor.execute("UPDATE books SET downloads_count = downloads_count + 1 WHERE id = ?", (book_id,))
        conn.commit()
        
        caption_text = (
            f"📘 <b>Nomi:</b> {book['title']}\n"
            f"📝 <b>Tavsif:</b> {book['description']}\n"
            f"📊 <b>Yuklangan:</b> {book['downloads_count'] + 1} marta\n\n"
            f"📥 EduAcademy tomonidan taqdim etildi."
        )
        
        # Bu yerda haqiqiy file_id yoziladi. Namuna sifatida matn qaytaramiz
        await call.message.answer(text=caption_text, parse_mode="HTML")
        await call.answer("Kitob ma'lumotlari muvaffaqiyatli yuklandi.", show_alert=False)
        
    except Exception as e:
        logger.error(f"view_book_callback da xato: {e}")
        await call.answer("Faylni yuklashda xatolik yuz berdi.", show_alert=True)
    finally:
        conn.close()
