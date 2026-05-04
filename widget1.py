import tkinter as tk
from tkinter import ttk
import psutil
import platform
from datetime import datetime

class SimpleSystemWidget:
    def __init__(self):
        # Создаем окно
        self.window = tk.Tk()
        self.window.title("System Monitor")
        self.window.geometry("400x500")
        self.window.attributes('-topmost', True)  # Всегда поверх других окон
        self.window.configure(bg='#1e1e1e')
        
        # Стили
        self.colors = {
            'bg': '#1e1e1e',
            'text': '#ffffff',
            'cpu': '#4caf50',
            'ram': '#2196f3',
            'disk': '#ff9800',
            'warning': '#f44336'
        }
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Запускаем обновление данных
        self.update_stats()
        
        # Запускаем главный цикл
        self.window.mainloop()
    
    def create_widgets(self):
        """Создает все элементы интерфейса"""
        
        # Заголовок
        title = tk.Label(
            self.window,
            text="📊 SYSTEM MONITOR",
            font=("Arial", 16, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title.pack(pady=10)
        
        # Информация о системе
        self.system_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg='#888888'
        )
        self.system_label.pack(pady=5)
        
        # === CPU ===
        cpu_frame = tk.Frame(self.window, bg=self.colors['bg'])
        cpu_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            cpu_frame,
            text="💻 CPU",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['cpu']
        ).pack(anchor='w')
        
        self.cpu_percent_label = tk.Label(
            cpu_frame,
            text="0%",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.cpu_percent_label.pack(anchor='w')
        
        # Прогресс-бар CPU
        self.cpu_bar = ttk.Progressbar(
            cpu_frame,
            length=350,
            mode='determinate',
            style='green.Horizontal.TProgressbar'
        )
        self.cpu_bar.pack(pady=5)
        
        # Дополнительная информация о CPU
        self.cpu_info_label = tk.Label(
            cpu_frame,
            text="",
            font=("Arial", 9),
            bg=self.colors['bg'],
            fg='#888888'
        )
        self.cpu_info_label.pack(anchor='w')
        
        # === RAM ===
        ram_frame = tk.Frame(self.window, bg=self.colors['bg'])
        ram_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            ram_frame,
            text="🧠 RAM",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['ram']
        ).pack(anchor='w')
        
        self.ram_percent_label = tk.Label(
            ram_frame,
            text="0%",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.ram_percent_label.pack(anchor='w')
        
        self.ram_bar = ttk.Progressbar(ram_frame, length=350, mode='determinate')
        self.ram_bar.pack(pady=5)
        
        self.ram_info_label = tk.Label(
            ram_frame,
            text="",
            font=("Arial", 9),
            bg=self.colors['bg'],
            fg='#888888'
        )
        self.ram_info_label.pack(anchor='w')
        
        # === DISK ===
        disk_frame = tk.Frame(self.window, bg=self.colors['bg'])
        disk_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            disk_frame,
            text="💾 DISK (C:)",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['disk']
        ).pack(anchor='w')
        
        self.disk_percent_label = tk.Label(
            disk_frame,
            text="0%",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.disk_percent_label.pack(anchor='w')
        
        self.disk_bar = ttk.Progressbar(disk_frame, length=350, mode='determinate')
        self.disk_bar.pack(pady=5)
        
        self.disk_info_label = tk.Label(
            disk_frame,
            text="",
            font=("Arial", 9),
            bg=self.colors['bg'],
            fg='#888888'
        )
        self.disk_info_label.pack(anchor='w')
        
        # === Дополнительная информация ===
        extra_frame = tk.Frame(self.window, bg=self.colors['bg'])
        extra_frame.pack(fill='x', padx=20, pady=10)
        
        # Батарея (если есть)
        self.battery_label = tk.Label(
            extra_frame,
            text="",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.battery_label.pack(anchor='w', pady=2)
        
        # Температура (если есть)
        self.temp_label = tk.Label(
            extra_frame,
            text="",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.temp_label.pack(anchor='w', pady=2)
        
        # Время обновления
        self.time_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 8),
            bg=self.colors['bg'],
            fg='#555555'
        )
        self.time_label.pack(side='bottom', pady=5)
    
    def get_size(self, bytes):
        """Конвертирует байты в ГБ/МБ"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"
    
    def update_stats(self):
        """Обновляет все показатели"""
        
        # === CPU ===
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_freq = psutil.cpu_freq()
        cpu_cores = psutil.cpu_count()
        
        self.cpu_percent_label.config(text=f"{cpu_percent:.0f}%")
        self.cpu_bar['value'] = cpu_percent
        
        # Цвет прогресс-бара CPU
        if cpu_percent > 80:
            self.cpu_bar['style'] = 'red.Horizontal.TProgressbar'
        elif cpu_percent > 60:
            self.cpu_bar['style'] = 'yellow.Horizontal.TProgressbar'
        else:
            self.cpu_bar['style'] = 'green.Horizontal.TProgressbar'
        
        freq_text = f"{cpu_freq.current/1000:.2f} GHz" if cpu_freq else "N/A"
        self.cpu_info_label.config(text=f"Frequency: {freq_text} | Cores: {cpu_cores}")
        
        # === RAM ===
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_used = self.get_size(ram.used)
        ram_total = self.get_size(ram.total)
        
        self.ram_percent_label.config(text=f"{ram_percent:.0f}%")
        self.ram_bar['value'] = ram_percent
        
        self.ram_info_label.config(text=f"Used: {ram_used} / {ram_total}")
        
        # === DISK ===
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used = self.get_size(disk.used)
        disk_total = self.get_size(disk.total)
        
        self.disk_percent_label.config(text=f"{disk_percent:.0f}%")
        self.disk_bar['value'] = disk_percent
        
        self.disk_info_label.config(text=f"Used: {disk_used} / {disk_total}")
        
        # === BATTERY (если есть) ===
        battery = psutil.sensors_battery()
        if battery:
            battery_percent = battery.percent
            plugged = "🔌 Charging" if battery.power_plugged else "🔋 Battery"
            self.battery_label.config(text=f"{plugged}: {battery_percent:.0f}%")
        else:
            self.battery_label.config(text="🔌 Desktop PC")
        
        # === TEMPERATURE (если есть) ===
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Пытаемся найти температуру CPU
                for name, entries in temps.items():
                    if 'core' in name.lower() or 'cpu' in name.lower() or 'k10' in name.lower():
                        temp = entries[0].current
                        self.temp_label.config(text=f"🌡️ CPU Temp: {temp:.1f}°C")
                        break
                else:
                    self.temp_label.config(text="")
            else:
                self.temp_label.config(text="")
        except:
            self.temp_label.config(text="")
        
        # === TIME ===
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Updated: {current_time}")
        
        # Обновляем каждую секунду
        self.window.after(1000, self.update_stats)

# Настройка стилей прогресс-баров
def setup_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("green.Horizontal.TProgressbar",
                    background='#4caf50',
                    troughcolor='#2d2d2d',
                    bordercolor='#2d2d2d',
                    lightcolor='#4caf50',
                    darkcolor='#4caf50')
    
    style.configure("yellow.Horizontal.TProgressbar",
                    background='#ffc107',
                    troughcolor='#2d2d2d',
                    bordercolor='#2d2d2d',
                    lightcolor='#ffc107',
                    darkcolor='#ffc107')
    
    style.configure("red.Horizontal.TProgressbar",
                    background='#f44336',
                    troughcolor='#2d2d2d',
                    bordercolor='#2d2d2d',
                    lightcolor='#f44336',
                    darkcolor='#f44336')

# Запуск
if __name__ == "__main__":
    setup_styles()
    SimpleSystemWidget()