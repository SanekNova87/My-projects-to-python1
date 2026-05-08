from database import get_connection

def recommend(answers):
    """ 
    Принимает словарь answers: {question_id: option_id}.
    Возвращает строку с названием и описанием рекомендационной сборки.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Извлекаем числовые параметры выбранных ответов
    param_values = {}
    for q_id, opt_id in answers.items():
        cur.execute("SELECT param_value FROM options WHERE id = ?", (opt_id,))
        row = cur.fetchone()
        if row:
            # Определяем, к какому типу параметра относится вопрос
            cur.execute("SELECT id FROM questions WHERE id = ?", (q_id,))
            question = cur.fetchone()
            # Зная порядок вопросов, можно определить, что это за параметр
            # У нас порядок: бюджет=1, задача=2, фича=3, процессор=4
            cur.execute("SELECT question_order FROM questions WHERE id = ?", (q_id,))
            order = cur.fetchone()[0]
            if order == 1:
                param_values['budget'] = row['param_value']
            elif order == 2:
                param_values['task'] = row['param_value']
            elif order == 3:
                param_values['feature'] = row['param_value']
            elif order == 4:
                param_values['cpu'] = row['param_value']

    # Ищем точное совпадение в таблице assemblies
    cur.execute(""" 
        SELECT name, description FROM assemblies
        WHERE budget_level = ? AND task_type = ? AND feature = ? AND cpu_brand = ?
    """, (param_values.get('budget', 1),
          param_values.get('task', 1),
          param_values.get('feature', 1),
          param_values.get('cpu', 1)))
    row = cur.fetchone()

    if row:
        result = f"{row['name']}\n\n{row['description']}"
    else:
        # Если нет точного човпадения - выдаем первую попавшуюся сборку
        cur.execute("SELECT name, description FROM assemblies LIMIT 1")
        row = cur.fetchone()
        result = f"Не удалось подобрать идеально.\nПредлагаем: {row['name']}\n\n{row['description']}"

    conn.close()
    return result