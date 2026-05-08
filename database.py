import sqlite3 
import json
import os
from datetime import datetime

# ============================================================
# НАСТРОЙКА ПУТИ К БАЗЕ ДАННЫХ
# ============================================================
# База данных будет создана в ПАПКЕ С ПРОГРАММОЙ
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(CURRENT_DIR, "exept.db")

def get_connection():
    """Устанавливает соединение с БД и настраивает формат строк."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Чтобы обращаться к полям по имени
    return conn

def init_db():
    """ 
    Создает таблицы (если их нет) и заполняет начальными данными.
    Вызывается один раз при старте программы.
    """    
    conn = get_connection()
    cur = conn.cursor()
    
    # Таблица вопросов
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            question_order INTEGER NOT NULL   
        );           
    """)

    # Таблица вариантов ответов
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            param_value INTEGER NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );
    """)   
    
    # Таблица готовых сборок ПК
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS assemblies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            budget_level INTEGER NOT NULL,
            task_type INTEGER NOT NULL,
            feature INTEGER NOT NULL,
            cpu_brand INTEGER NOT NULL
        );           
    """)    
    
    # Таблица истории запросов 
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            answers_json TEXT NOT NULL,
            result TEXT NOT NULL    
        );           
    """)   

    # Проверяем, есть ли уже данные в таблице вопросов
    cur.execute("SELECT COUNT(*) FROM questions")
    if cur.fetchone()[0] == 0:
        # Вопрос 1 (бюджет)
        cur.execute("INSERT INTO questions (text, question_order) VALUES (?, ?)",
                    ("Какой у вас бюджет?", 1))
        q1_id = cur.lastrowid
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q1_id, "До 50 000 руб.", 1))
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q1_id, "50 000 - 100 000 руб.", 2))
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q1_id, "Более 100 000 руб.", 3))
        
        # Вопрос 2 (назначение)
        cur.execute("INSERT INTO questions (text, question_order) VALUES (?, ?)",
                    ("Для чего вам нужен компьютер?", 2))
        q2_id = cur.lastrowid
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q2_id, "Офисная работа, интернет.", 1))
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q2_id, "Игры.", 2))
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q2_id, "Дизайн, видеомонтаж.", 3))
        
        # Вопрос 3 (дополнительное пожелание)
        cur.execute("INSERT INTO questions (text, question_order) VALUES (?, ?)",
                    ("Что для вас важнее всего?", 3))
        q3_id = cur.lastrowid
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q3_id, "Тихая работа.", 1))
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q3_id, "Компактный корпус.", 2))
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q3_id, "Максимальная производительность.", 3))
        
        # Вопрос 4 (предпочтительный процессор)
        cur.execute("INSERT INTO questions (text, question_order) VALUES (?, ?)",
                    ("Предпочтение по процессору?", 4))
        q4_id = cur.lastrowid
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q4_id, "Intel.", 1))
        cur.execute("INSERT INTO options (question_id, text, param_value) VALUES (?, ?, ?)",
                    (q4_id, "AMD.", 2))      
        
        # Заполняем таблицу сборок (все возможные комбинации)
        assemblies_data = [
            # budget_level = 1 (бюджетный), task_type = 1 (офис)
            (1, 1, 1, 1, "Офис-Тихий (бюджет)", "Intel Core i3, 8 ГБ RAM, SSD 256 ГБ, без вентиляторов"),
            (1, 1, 2, 1, "Офис-Компакт (бюджет)", "Intel Core i3, 8 ГБ RAM, SSD 256 ГБ, корпус Mini-ITX"),
            (1, 1, 3, 1, "Офис-Произв (бюджет)", "Intel Core i3, 16 ГБ RAM, SSD 512 ГБ"),
            # budget_level = 1 (бюджетный), task_type = 2 (игры)
            (1, 2, 1, 2, "Игры-Тихий (бюджет)", "AMD Ryzen 3, 16 ГБ RAM, GTX 1650, тихий кулер"),
            (1, 2, 2, 2, "Игры-Компакт (бюджет)", "AMD Ryzen 3, 16 ГБ RAM, GTX 1650, компактный корпус"),
            (1, 2, 3, 2, "Игры-Произв (бюджет)", "AMD Ryzen 5, 16 ГБ RAM, GTX 1660 Super"),
            # budget_level = 2 (средний)
            (2, 1, 1, 1, "Офис-Тихий (средний)", "Intel Core i5, 16 ГБ RAM, SSD 512 ГБ, пассивное охлаждение"),
            (2, 1, 2, 1, "Офис-Компакт (средний)", "Intel Core i5, 16 ГБ RAM, SSD 512 ГБ, Mini-ITX"),
            (2, 1, 3, 1, "Офис-Произв (средний)", "Intel Core i5, 32 ГБ RAM, SSD 1 ТБ"),
            (2, 2, 1, 1, "Игры-Тихий (средний)", "Intel Core i5, 32 ГБ RAM, SSD 512 ГБ, водяное охлаждение"),
            (2, 2, 2, 1, "Игры-Компакт (средний)", "Intel Core i5, 32 ГБ RAM, RTX 3070, компактный корпус"),
            (2, 2, 3, 1, "Игры-Произв (средний)", "Intel Core i7, 32 ГБ RAM, RTX 3070"),
            (2, 3, 1, 2, "Дизайн-Тихий (средний)", "AMD Ryzen 7, 64 ГБ RAM, RTX 3060, тихое охлаждение"),
            (2, 3, 2, 2, "Дизайн-Компакт (средний)", "AMD Ryzen 7, 64 ГБ RAM, RTX 3060, Mini-ITX"),
            (2, 3, 3, 2, "Дизайн-Произв (средний)", "AMD Ryzen 7, 64 ГБ RAM, RTX 3060"),
            # budget_level = 3 (высокий)
            (3, 1, 1, 1, "Офис-Тихий (высокий)", "Intel Core i7, 64 ГБ RAM, SSD 2 ТБ, безвентиляторный корпус"),
            (3, 1, 2, 1, "Офис-Компакт (высокий)", "Intel Core i7, 64 ГБ RAM, SSD 2 ТБ, Mini-ITX"),
            (3, 1, 3, 1, "Офис-Произв (высокий)", "Intel Core i9, 64 ГБ RAM, SSD 2 ТБ"),
            (3, 2, 1, 1, "Игры-Тихий (высокий)", "Intel Core i9, 64 ГБ RAM, RTX 4080, жидкостное охлаждение"),
            (3, 2, 2, 1, "Игры-Компакт (высокий)", "Intel Core i9, 64 ГБ RAM, RTX 4080, компактный корпус"),
            (3, 2, 3, 1, "Игры-Произв (высокий)", "Intel Core i9, 128 ГБ RAM, RTX 4080"),
            (3, 3, 1, 2, "Дизайн-Тихий (высокий)", "AMD Ryzen 9, 64 ГБ RAM, RTX 4080, тихая система"),
            (3, 3, 2, 2, "Дизайн-Компакт (высокий)", "AMD Ryzen 9, 64 ГБ RAM, RTX 4080, Mini-ITX"),
            (3, 3, 3, 2, "Дизайн-Произв (высокий)", "AMD Ryzen 9, 128 ГБ RAM, RTX 4080"),
        ]

        for (budget, task, feat, cpu, name, desc) in assemblies_data:
            cur.execute("""
                INSERT INTO assemblies (budget_level, task_type, feature, cpu_brand, name, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (budget, task, feat, cpu, name, desc))
        
        conn.commit()
    
    conn.close()

# Вспомогательные функции для GUI

def get_questions():
    """ Возвращает список вопросов, упорядоченный по question_order""" 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions ORDER BY question_order")
    questions = [dict(row) for row in cur.fetchall()]
    conn.close()
    return questions

def get_options(question_id):
    """ Возвращает список вариантов ответа для заданного вопроса""" 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM options WHERE question_id = ?", (question_id,))
    options = [dict(row) for row in cur.fetchall()]
    conn.close()
    return options

def save_history(answers_dict, result_text):
    """ Сохраняет результаты опроса в таблицу history""" 
    conn = get_connection()
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answers_json = json.dumps(answers_dict, ensure_ascii=False)
    cur.execute("INSERT INTO history (timestamp, answers_json, result) VALUES (?, ?, ?)",
                (timestamp, answers_json, result_text))
    conn.commit()
    conn.close()

# ============================================================
# ПРИ ЗАПУСКЕ ЭТОГО ФАЙЛА СОЗДАЕТСЯ БАЗА ДАННЫХ
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("Создание базы данных для экспертной системы")
    print("=" * 50)
    print(f"Путь к файлу: {DB_NAME}")
    print()
    
    init_db()
    
    # Проверяем, что файл создан
    if os.path.exists(DB_NAME):
        print()
        print("=" * 50)
        print("РЕЗУЛЬТАТ:")
        print("=" * 50)
        print(f"✅ База данных успешно создана!")
        print(f"✅ Файл: {DB_NAME}")
        print(f"✅ Размер: {os.path.getsize(DB_NAME)} байт")
        
        # Показываем статистику
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM questions")
        questions_count = cur.fetchone()[0]
        print(f"✅ Вопросов: {questions_count}")
        
        cur.execute("SELECT COUNT(*) FROM options")
        options_count = cur.fetchone()[0]
        print(f"✅ Вариантов ответов: {options_count}")
        
        cur.execute("SELECT COUNT(*) FROM assemblies")
        assemblies_count = cur.fetchone()[0]
        print(f"✅ Готовых сборок: {assemblies_count}")
        
        cur.execute("SELECT COUNT(*) FROM history")
        history_count = cur.fetchone()[0]
        print(f"✅ Записей в истории: {history_count}")
        
        conn.close()
        print()
        print("✅ Готово! Можете запускать основную программу.")
    else:
        print()
        print("❌ ОШИБКА: База данных не была создана!")