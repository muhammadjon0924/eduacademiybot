from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
import sqlite3
import random
from database.connections import get_db_connection

router = Router()
logger = logging.getLogger(__name__)

class TestStates(StatesGroup):
    solving = State()

def get_tests_keyboard(tests_list):
    """Mavjud testlar katalogi uchun inline tugmalar yaratish"""
    builder = InlineKeyboardBuilder()
    for test in tests_list:
        builder.row(types.InlineKeyboardButton(
            text=f"📝 {test['title']}", 
            callback_data=f"start_test_{test['id']}"
        ))
    return builder.as_markup()

def get_options_keyboard(question_dict):
    """Variantlarni aralashtirib yoki tartib bilan chiqaradigan tugmalar"""
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="A", callback_data="ans_A"),
        types.InlineKeyboardButton(text="B", callback_data="ans_B"),
        types.InlineKeyboardButton(text="C", callback_data="ans_C"),
        types.InlineKeyboardButton(text="D", callback_data="ans_D")
    )
    return builder.as_markup()

@router.message(F.text == "📝 Testlar")
async def tests_handler(message: types.Message, state: FSMContext):
    """Tizimdagi barcha faol testlarni foydalanuvchiga taqdim etish"""
    await state.clear()
    
    conn = get_db_connection()
    if not conn:
        await message.answer("⚠️ Ma'lumotlar bazasi bilan aloqa uzildi.")
        return
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, questions_count FROM tests WHERE is_active = 1")
        active_tests = cursor.fetchall()
        
        if not active_tests:
            await message.answer(
                "📝 <b>Online Bilim Sinash Bo'limi</b>\n\nHozirda faol imtihonlar yo'q.",
                parse_mode="HTML"
            )
            return
            
        text = (
            "📝 <b>Online Imtihon Topshirish Bo'limi</b>\n\n"
            "O'z bilimingizni sinab ko'rish va reytingingizni oshirish uchun quyidagi test bloklaridan birini tanlang:\n\n"
            "⚠️ <i>Eslatma: Test yakunlangach natijalar shaxsiy kabinetingizda saqlanadi!</i>"
        )
        await message.answer(text=text, parse_mode="HTML", reply_markup=get_tests_keyboard(active_tests))
        
    except Exception as e:
        logger.error(f"Testlar bo'limida xatolik: {e}")
        await message.answer("⚠️ Ma'lumotlarni yuklashda xatolik yuz berdi.")
    finally:
        conn.close()

@router.callback_query(F.data.startswith("start_test_"))
async def start_test_callback(call: types.CallbackQuery, state: FSMContext):
    """Foydalanuvchi testni tanlaganda birinchi savolni chiqarish"""
    test_id = int(call.data.split("_")[2])
    
    conn = get_db_connection()
    if not conn:
        await call.answer("Baza ulanish xatosi!", show_alert=True)
        return
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM tests WHERE id = ?", (test_id,))
        test = cursor.fetchone()
        
        cursor.execute("SELECT * FROM questions WHERE test_id = ?", (test_id,))
        questions = [dict(row) for row in cursor.fetchall()]
        
        if not questions:
            await call.answer("Ushbu testda hali savollar mavjud emas!", show_alert=True)
            return
            
        # Savollarni tasodifiy tartibda aralashtirish (Variantni qiziqarli qilish uchun)
        random.shuffle(questions)
        
        await state.update_data(
            test_id=test_id,
            test_title=test['title'],
            questions=questions,
            current_index=0,
            score=0,
            total=len(questions)
        )
        
        await state.set_state(TestStates.solving)
        await call.message.delete()
        
        # Birinchi savol
        await send_question(call.message, questions[0], 1, len(questions))
        await call.answer()
        
    except Exception as e:
        logger.error(f"start_test_callback da xato: {e}")
        await call.answer("Xatolik yuz berdi.", show_alert=True)
    finally:
        conn.close()

async def send_question(message: types.Message, question_dict, current_num, total_num):
    """Savol va uning variantlarini chiroyli ko'rinishda jo'natish"""
    text = (
        f"📋 <b>Savol {current_num} / {total_num}</b>\n\n"
        f"❓ <b>{question_dict['question_text']}</b>\n\n"
        f"<b>A)</b> {question_dict['option_a']}\n"
        f"<b>B)</b> {question_dict['option_b']}\n"
        f"<b>C)</b> {question_dict['option_c']}\n"
        f"<b>D)</b> {question_dict['option_d']}\n\n"
        f"👇 To'g'ri deb bilgan javob variantingizni tanlang:"
    )
    await message.answer(text=text, parse_mode="HTML", reply_markup=get_options_keyboard(question_dict))

@router.callback_query(TestStates.solving, F.data.startswith("ans_"))
async def handle_answer_callback(call: types.CallbackQuery, state: FSMContext):
    """Variant tanlanganda javobni tekshirish va keyingi bosqichga o'tkazish"""
    user_answer = call.data.split("_")[1] # A, B, C yoki D
    
    data = await state.get_data()
    questions = data['questions']
    current_index = data['current_index']
    score = data['score']
    total = data['total']
    test_id = data['test_id']
    
    current_question = questions[current_index]
    
    if user_answer == current_question['correct_option']:
        score += 1
        
    current_index += 1
    await state.update_data(score=score, current_index=current_index)
    
    await call.message.delete()
    
    if current_index < total:
        await send_question(call.message, questions[current_index], current_index + 1, total)
    else:
        # Natijani bazaga yozish
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO test_results (telegram_id, test_id, score, total_questions) VALUES (?, ?, ?, ?)",
                (call.from_user.id, test_id, score, total)
            )
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Natijani saqlashda muammo: {e}")
        finally:
            conn.close()
            
        foiz = (score / total) * 100
        result_text = (
            f"🏁 <b>Imtihon yakunlandi!</b>\n\n"
            f"🏆 <b>Test:</b> {data['test_title']}\n"
            f"✅ <b>To'g'ri javoblar:</b> {score} / {total} ta\n"
            f"📊 <b>Natijangiz:</b> {foiz:.1f}%\n\n"
            f"💡 Muvaffaqiyatli topshirdingiz! Natijani istalgan vaqtda <b>👤 Shaxsiy Kabinet</b> orqali tekshirishingiz mumkin."
        )
        await call.message.answer(text=result_text, parse_mode="HTML")
        await state.clear()
        
    await call.answer()