import sqlite3
import logging
from config.settings import DB_PATH

logger = logging.getLogger(__name__)

def init_db():
    """Ma'lumotlar bazasini professional arxitekturada yaratish va savollar bilan to'ldirish"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Foydalanuvchilar jadvali
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            username TEXT,
            status TEXT DEFAULT 'active',
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 2. Kitoblar jadvali
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            file_id TEXT NOT NULL,
            downloads_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 3. Testlar jadvali
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            questions_count INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 4. Savollar jadvali
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL, -- 'A', 'B', 'C', yoki 'D'
            FOREIGN KEY (test_id) REFERENCES tests(id)
        )
        """)
        
        # 5. Natijalar jadvali
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            test_id INTEGER,
            score INTEGER,
            total_questions INTEGER,
            solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id),
            FOREIGN KEY (test_id) REFERENCES tests(id)
        )
        """)
        
        # Jadvallardagi eski noto'g'ri ma'lumotlarni tozalash (Xavfsiz qayta yuklash uchun)
        cursor.execute("DELETE FROM questions")
        cursor.execute("DELETE FROM tests")
        
        # YANGI PROFESSIONAL TESTLAR VA SAVOLLAR:
        
        # --- 1-FAN: MATEMATIKA (ID: 1) ---
        cursor.execute("INSERT INTO tests (id, title, questions_count) VALUES (1, 'Matematika fanidan test (10 ta savol)', 10)")
        
        matematika_savollari = [
            ("5 * 5 - 5 amalini bajaring.", "20", "25", "15", "10", "A"),
            ("Kvadratning yuzi 64 sm² bo'lsa, uning tomoni uzunligini toping.", "8 sm", "16 sm", "4 sm", "32 sm", "A"),
            ("Qaysi son barcha sonlarga bo'linadi?", "0", "1", "2", "Hech qaysi", "A"),
            ("120 ning 10% ini toping.", "12", "1.2", "20", "10", "A"),
            ("Eng kichik tub sonni ko'rsating.", "2", "1", "3", "0", "A"),
            ("Uchburchakning ichki burchaklari yig'indisi nechaga teng?", "180°", "360°", "90°", "270°", "A"),
            ("x + 15 = 40 bo'lsa, x ning qiymatini toping.", "25", "35", "15", "30", "A"),
            ("Doiraning yuzi formulasini ko'rsating.", "S = πr²", "S = 2πr", "S = ab", "S = a²", "A"),
            ("100 sonining kvadrat ildizini toping.", "10", "50", "20", "5", "A"),
            ("Agar poyezd 2 soatda 160 km yursa, uning tezligi qancha?", "80 km/h", "60 km/h", "100 km/h", "90 km/h", "A")
        ]
        for q in matematika_savollari:
            cursor.execute("""
                INSERT INTO questions (test_id, question_text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (1, ?, ?, ?, ?, ?, ?)
            """, q)

        # --- 2-FAN: ONA TILI VA ADABIYOT (ID: 2) ---
        cursor.execute("INSERT INTO tests (id, title, questions_count) VALUES (2, 'Ona tili va adabiyot (15 ta savol)', 15)")
        
        ona_tili_savollari = [
            ("O'zbek adabiy tilining asoschisi kim?", "Alisher Navoiy", "Bobur", "Abdulla Qodiriy", "Cho'lpon", "A"),
            ("Sifat so'z turkumi qanday so'roqlarga javob bo'ladi?", "Qanday?, Qanaqa?", "Kim?, Nima?", "Nechta?, Qancha?", "Qachon?", "A"),
            ("'Sariq devni minib' asari muallifi kim?", "Xudoyberdi To'xtaboyev", "O'tkir Hoshimov", "G'afur G'ulom", "Abdulla Qahhor", "A"),
            ("O'zbekiston Respublikasining Davlat tili haqidagi qonuni qachon qabul qilingan?", "1989-yil 21-oktabr", "1991-yil 31-avgust", "1992-yil 8-dekabr", "1993-yil 2-sentabr", "A"),
            ("Ot so'z turkumi nimalarni bildiradi?", "Shaxs va narsani", "Harakatni", "Belgini", "Miqdorni", "A"),
            ("'O'tkan kunlar' romani qachon yozilgan?", "1922-yil", "1915-yil", "1930-yil", "1926-yil", "A"),
            ("O'zbek tilida nechta unli tovush bor?", "6 ta", "10 ta", "5 ta", "8 ta", "A"),
            ("Eshik, kitob, qalam so'zlari qaysi so'z turkumiga kiradi?", "Ot", "Sifat", "Fe'l", "Son", "A"),
            ("Adabiyotda birinchi o'zbek romanini kim yozgan?", "Abdulla Qodiriy", "Hamid Olimjon", "Oybek", "G'afur G'ulom", "A"),
            ("Fe'l turkumi nima bildiradi?", "Ish-harakatni", "Narsaning nomini", "Narsaning belgisini", "Narsaning miqdorini", "A"),
            ("Sodda gapda nechta kesim bo'ladi?", "1 ta", "2 ta", "3 ta", "Ko'p", "A"),
            ("O'zbek alifbosida nechta harf bor?", "29 ta", "30 ta", "26 ta", "32 ta", "A"),
            ("'Shum bola' qissasining muallifi kim?", "G'afur G'ulom", "Abdulla Qahhor", "Oybek", "Said Ahmad", "A"),
            ("Gapning bosh bo'laklari qaysilar?", "Ega va kesim", "Ega va to'ldiruvchi", "Hol va aniqlovchi", "Kesim va hol", "A"),
            ("Sinonim so'zlar nima?", "Ma'nodosh so'zlar", "Shakldosh so'zlar", "Zid ma'noli so'zlar", "Talaffuzdosh so'zlar", "A")
        ]
        for q in ona_tili_savollari:
            cursor.execute("""
                INSERT INTO questions (test_id, question_text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (2, ?, ?, ?, ?, ?, ?)
            """, q)

        # --- 3-FAN: INGLIZ TILI (ID: 3) ---
        cursor.execute("INSERT INTO tests (id, title, questions_count) VALUES (3, 'Ingliz tili - CEFR B2 (20 ta savol)', 20)")
        
        ingliz_tili_savollari = [
            ("She ... to school every day.", "goes", "go", "going", "went", "A"),
            ("What is the synonym of 'Beautiful'?", "Pretty", "Ugly", "Sad", "Angry", "A"),
            ("Identify the past simple form of 'Write'.", "Wrote", "Written", "Writes", "Writing", "A"),
            ("If I ... you, I would study harder.", "were", "am", "was", "be", "A"),
            ("We have been living here ... 2018.", "since", "for", "during", "in", "A"),
            ("This is the ... book I have ever read.", "best", "good", "better", "most good", "A"),
            ("They ... football when it started to rain.", "were playing", "played", "are playing", "play", "A"),
            ("What is the opposite of 'Generous'?", "Mean", "Kind", "Happy", "Polite", "A"),
            ("He is interested ... learning languages.", "in", "at", "on", "about", "A"),
            ("I can't afford ... a new car.", "to buy", "buying", "buy", "bought", "A"),
            ("By next year, she ... from university.", "will have graduated", "will graduate", "graduates", "is graduating", "A"),
            ("Would you mind ... the window?", "closing", "to close", "close", "closed", "A"),
            ("The book ... by Shakespeare.", "was written", "wrote", "was writing", "written", "A"),
            ("You ... drive on the left in the UK.", "must", "should", "can", "may", "A"),
            ("What is the noun form of 'Decide'?", "Decision", "Decisive", "Decidedly", "Deciding", "A"),
            ("I wish I ... more time to study.", "had", "have", "will have", "am having", "A"),
            ("He apologized ... being late.", "for", "to", "on", "with", "A"),
            ("They decided to ... off the meeting.", "put", "take", "call", "run", "A"),
            ("That is the man ... car was stolen.", "whose", "who", "whom", "which", "A"),
            ("She is looking forward to ... you.", "seeing", "see", "seen", "saw", "A")
        ]
        for q in ingliz_tili_savollari:
            cursor.execute("""
                INSERT INTO questions (test_id, question_text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (3, ?, ?, ?, ?, ?, ?)
            """, q)

        conn.commit()
        print("💾 [DATABASE] Barcha 3 ta fandan jami 45 ta professional savollar yuklandi!")
    except sqlite3.Error as e:
        logger.error(f"Ma'lumotlar bazasini yaratishda xato: {e}")
        raise e
    finally:
        conn.close()

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Bazaga ulanishda xato yuz berdi: {e}")
        return None

def add_user(tg_id, full_name, username):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (telegram_id, full_name, username) 
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET 
                full_name = excluded.full_name,
                username = excluded.username
        """, (tg_id, full_name, username))
        conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"add_user da xato: {e}")
        return False
    finally:
        conn.close()