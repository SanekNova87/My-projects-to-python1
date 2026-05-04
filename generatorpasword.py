import json
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Manager")
        self.window.geometry("600x400")
        
        # Загружаем данные
        try:
            with open('passwords.json', 'r') as f:
                self.passwords = json.load(f)
        except:
            self.passwords = {}
        
        self.create_widgets()
        self.refresh_list()
        self.window.mainloop()
    
    def create_widgets(self):
        # Левая панель - список сервисов
        left_frame = tk.Frame(self.window, width=200)
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        tk.Label(left_frame, text="Сервисы:", font=("Arial", 12, "bold")).pack()
        
        self.service_listbox = tk.Listbox(left_frame, height=15)
        self.service_listbox.pack(fill='both', expand=True)
        self.service_listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Правая панель - детали
        right_frame = tk.Frame(self.window)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Поля ввода
        tk.Label(right_frame, text="Сервис:", font=("Arial", 10)).pack(anchor='w')
        self.service_entry = tk.Entry(right_frame, width=30)
        self.service_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(right_frame, text="Логин:", font=("Arial", 10)).pack(anchor='w')
        self.login_entry = tk.Entry(right_frame, width=30)
        self.login_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(right_frame, text="Пароль:", font=("Arial", 10)).pack(anchor='w')
        self.password_entry = tk.Entry(right_frame, width=30)
        self.password_entry.pack(fill='x', pady=(0, 10))
        
        # Кнопки
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="➕ Добавить", command=self.add_password,
                 bg='#27ae60', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑 Удалить", command=self.delete_password,
                 bg='#e74c3c', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔀 Сгенерировать", command=self.generate_password,
                 bg='#3498db', fg='white').pack(side='left', padx=5)
        
        # Кнопка показать/скрыть пароль
        self.show_password = False
        tk.Button(right_frame, text="👁 Показать пароль", command=self.toggle_show,
                 bg='#f39c12', fg='white').pack(fill='x')
    
    def generate_password(self):
        """Генерирует случайный пароль"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(12))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
    
    def add_password(self):
        """Добавляет новый пароль"""
        service = self.service_entry.get().strip()
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not service or not login or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        
        self.passwords[service] = {'login': login, 'password': password}
        self.save_passwords()
        self.refresh_list()
        self.clear_fields()
        messagebox.showinfo("Успех", "Пароль сохранен!")
    
    def delete_password(self):
        """Удаляет выбранный пароль"""
        selection = self.service_listbox.curselection()
        if selection:
            service = self.service_listbox.get(selection[0])
            del self.passwords[service]
            self.save_passwords()
            self.refresh_list()
            self.clear_fields()
    
    def on_select(self, event):
        """Показывает данные выбранного сервиса"""
        selection = self.service_listbox.curselection()
        if selection:
            service = self.service_listbox.get(selection[0])
            data = self.passwords[service]
            self.service_entry.delete(0, tk.END)
            self.service_entry.insert(0, service)
            self.login_entry.delete(0, tk.END)
            self.login_entry.insert(0, data['login'])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, data['password'])
    
    def toggle_show(self):
        """Показывает/скрывает пароль"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')
    
    def clear_fields(self):
        """Очищает поля ввода"""
        self.service_entry.delete(0, tk.END)
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def refresh_list(self):
        """Обновляет список сервисов"""
        self.service_listbox.delete(0, tk.END)
        for service in sorted(self.passwords.keys()):
            self.service_listbox.insert(tk.END, service)
    
    def save_passwords(self):
        """Сохраняет пароли в файл"""
        with open('passwords.json', 'w') as f:
            json.dump(self.passwords, f, indent=2)

if __name__ == "__main__":
    PasswordManager()