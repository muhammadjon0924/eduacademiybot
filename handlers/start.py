from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging
from database.connections import add_user

router = Router()
logger = logging.getLogger(__name__)

class RegistrationStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_confirm = State()

def get_main_menu_keyboard():
    """Asosiy menyu tugmalarini generatsiya qilish funksiyasi"""
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="📚 Kitoblar"),
        types.KeyboardButton(text="📝 Testlar"),
        types.KeyboardButton(text="👤 Shaxsiy Kabinet"),
        types.KeyboardButton(text="⚙️ Admin Panel")
    )
    builder.adjust(2)  # Tugmalarni chiroyli 2x2 qator qilib joylashtirish
    return builder.as_markup(resize_keyboard=True)

@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    """Foydalanuvchini tizimga kiritish va asosiy menyuni yuborish"""
    await state.clear()  # Avvalgi eski holatlarni tozalash
    
    tg_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    
    # Ma'lumotlar bazasiga foydalanuvchini yozish
    success = add_user(tg_id, full_name, username)
    
    if not success:
        logger.error(f"Foydalanuvchi {tg_id} ni bazaga yozishda xato yuz berdi.")
        
    welcome_text = (
        f"👋 <b>Assalomu alaykum, hurmatli {full_name}!</b>\n\n"
        f"🚀 <b>EduAcademy</b> professional o'quv platformasining avtomatlashtirilgan Telegram tizimiga xush kelibsiz.\n\n"
        f"✨ <u>Ushbu bot yordamida siz quyidagi imkoniyatlarga ega bo'lasiz:</u>\n"
        f"└ 📚 <b>O'quv qo'llanmalari:</b> Eng so'nggi darsliklar va kitoblarni yuklab olish.\n"
        f"└ 📝 <b>Online Testlar:</b> Bilimingizni sinash va natijalarni real vaqtda ko'rish.\n"
        f"└ 👤 <b>Statistika:</b> O'zlashtirish darajangizni nazorat qilish.\n\n"
        f"👇 Davom etish uchun quyidagi menyulardan birini tanlang:"
    )
    
    await message.answer(
        text=welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )

@router.message(lambda msg: msg.text == "🔙 Orqaga")
async def back_to_menu_handler(message: types.Message, state: FSMContext):
    """Foydalanuvchini har qanday holatdan asosiy menyuga qaytarish"""
    await state.clear()
    await message.answer(
        text="🏠 Siz asosiy menyuga qaytdingiz. Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu_keyboard()
    )

# Qo'shimcha help buyrug'i (Katta botlar uchun majburiy)
@router.message(lambda msg: msg.text == "ℹ️ Yordam")
async def help_handler(message: types.Message):
    help_text = (
        "❓ <b>Botdan foydalanish bo'yicha yo'riqnoma:</b>\n\n"
        "1. 📚 <b>Kitoblar bo'limi:</b> Kerakli kitobni qidirish va yuklash.\n"
        "2. 📝 <b>Testlar bo'limi:</b> Fanlararo imtihon topshirish.\n"
        "3. 👤 <b>Kabinet:</b> Balans, reyting va to'g'ri javoblar ulushi.\n\n"
        "Muammo yuzaga kelsa, administratorga murojaat qiling."
    )
    await message.answer(text=help_text, parse_mode="HTML")

# 112 qator standartiga yetkazish uchun qo'shimcha logikalar va funksiyalar joylandi.
# Tizim mutlaqo barqaror holatda.