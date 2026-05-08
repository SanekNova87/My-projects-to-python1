import os
import sys

# ============================================================
# ПРАВИЛЬНЫЙ ПУТЬ К ПЛАГИНАМ (найден автоматически)
# ============================================================
PLUGINS_PATH = r"C:\Users\Пользователь\AppData\Local\Programs\Python\Python313\Lib\site-packages\PyQt5\Qt5\plugins"

# Проверяем и устанавливаем переменную окружения
if os.path.exists(PLUGINS_PATH):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = PLUGINS_PATH
    print(f"✅ Плагины найдены: {PLUGINS_PATH}")
else:
    print(f"❌ ОШИБКА: Папка с плагинами не найдена")

# ============================================================
# Импортируем PyQt5
# ============================================================
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget,
                             QWidget, QVBoxLayout, QLabel, QPushButton,
                             QButtonGroup, QRadioButton, QMessageBox)
from PyQt5.QtCore import Qt
import database as db
from engine import recommend

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Экспертная система подбора ПК")
        self.setMinimumSize(500, 350)
        # Здесь будет храниться словарь ответов: {question_id: option_id}
        self.answers = {}

        # Центральный виджет, переключает страницы
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Инициализация БД (создание таблиц и наполнение, если нужно)
        db.init_db()

        # Строим интерфейс
        self.init_ui()

    def init_ui(self):
        """ Создает все страницы и добавляет их в stack."""
        # Страница приветствия 
        self.start_page = self.create_start_page()
        self.stack.addWidget(self.start_page)

        # Страница вопросов (динамически создаются по данным БД)
        self.question_pages = []
        questions = db.get_questions()
        for i, q in enumerate(questions):
            page = self.create_question_page(q)
            self.stack.addWidget(page)
            self.question_pages.append(page)

        # Страница результатов (пока пустая)
        self.result_page = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_page.setLayout(self.result_layout)
        self.stack.addWidget(self.result_page)

        # Показываем стартовую страницу
        self.stack.setCurrentIndex(0)

    def create_start_page(self):
        """ Создает страницу с приветствием и кнопкой 'Начать'."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Добро пожаловать!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        subtitle = QLabel("Эта программа поможет подобрать оптимальную конфигурацию ПК\nна основе ваших ответов.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        btn_start = QPushButton("Начать подбор")
        btn_start.setMinimumHeight(40)
        btn_start.clicked.connect(self.go_to_firts_question)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(btn_start)
        page.setLayout(layout)
        return page 
    
    def create_question_page(self, question):
        """ 
        Создает страницу одного вопроса.
        question - словарь с ключамии 'id', 'text', 'question_order'.
        """
        page = QWidget()
        layout = QVBoxLayout()
        lable = QLabel(question['text'])
        lable.setWordWrap(True)
        lable.setStyleSheet("font-size: 14px;")
        layout.addWidget(lable)

        # Группа радиокнопок для вариантов ответа
        options = db.get_options(question['id'])
        self.radio_groups = getattr(self, 'radio_groups', {})
        group = QButtonGroup(page)
        self.radio_groups[question['id']] = group # сохраним, чтобы потом проверять

        for opt in options:
            rb = QRadioButton(opt['text'])
            rb.option_id = opt['id'] # запоминаем id варианта прямо в кнопке
            group.addButton(rb)
            layout.addWidget(rb)

        # Кнопка "Далее"
        btn_next = QPushButton("Далее")
        btn_next.clicked.connect(lambda: self.next_question(question))
        layout.addStretch()
        layout.addWidget(btn_next)

        page.setLayout(layout)
        return page
    
    def go_to_firts_question(self):
        """ Переключаем на первый вопрос (индекс 1 в stack)."""
        self.stack.setCurrentIndex(1)

    def next_question(self, question):
        """ 
        Обрабатывает нажатие 'далее' на странице вопроса.
        Проверяет, выбран ли вариант, сохраняет ответ и переходит дальше.
        """
        group =self.radio_groups.get(question['id'])
        if group is None:
            return
        checked = group.checkedButton()
        if checked is None:
            QMessageBox.warning(self, "Внимание!", "Пожалуйста, выберите один из вариантов.")
            return
        
        # Сохраняем ответ
        self.answers[question['id']] = checked.option_id

        # Определяем текущий индекс
        current_idx = self.stack.currentIndex()

        # Если это был последний вопрос (индекс равен количеству страниц вопросов),
        # то переходим на страницу результата
        if current_idx == len(self.question_pages):
            self.show_result()
        else:
            # Иначе идем на следующую страницу
            self.stack.setCurrentIndex(current_idx + 1)

    def show_result(self):
        """ Показывает итоговую рекомендацию и сохраняет историю."""
        # Получаем результат от движка
        result_text = recommend(self.answers)

        # Очищаем страницу результата и наполняем ее
        for i in reversed(range(self.result_layout.count())):
            self.result_layout.itemAt(i).widget().setParent(None)
        
        label_result = QLabel("Рекомендованная сборка:")
        label_result.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.result_layout.addWidget(label_result)

        label_config = QLabel(result_text)
        label_config.setWordWrap(True)
        self.result_layout.addWidget(label_config)

        # Сохраняем запрос в историю
        db.save_history(self.answers, result_text)

        # Опционально: кнопка "Начать заново"
        btn_restart = QPushButton("Пройти заново")
        btn_restart.clicked.connect(self.restart)
        self.result_layout.addWidget(btn_restart)

        self.stack.setCurrentWidget(self.result_page)

    def restart(self):
        """ Сбрасывает ответы и возвращает на стартовую страницу."""
        self.answers.clear()
        # Очищаем выбор радиокнопок во всех группах
        for group in self.radio_groups.values():
            btn = group.checkedButton()
            if btn:
                group.setExclusive(False)
                btn.setChecked(False)
                group.setExclusive(True)
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())