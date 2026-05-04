import tkinter as tk
import psutil
from datetime import datetime

def get_size(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def get_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            return temps['coretemp'][0].current
        return "N/A"
    except:
        return "N/A"

def get_battery():
    try:
        battery = psutil.sensors_battery()
        return f"{battery.percent}% ({'⚡' if battery.power_plugged else '🔋'})"
    except:
        return "N/A"

def update_stats():
    # Время работы системы
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    
    # CPU
    cpu_percent = psutil.cpu_percent()
    cpu_count = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq().current / 1000
    cpu_temp = get_temperature()
    
    # RAM
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Диски
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    
    # Сеть
    net_io = psutil.net_io_counters()
    
    # Процессы
    processes = len(psutil.pids())
    
    # Формируем текст
    stats_text = (
        f"🕒 Uptime: {str(uptime).split('.')[0]}\n"
        f"🔋 Battery: {get_battery()}\n\n"
        
        f"🖥️ CPU: {cpu_percent}% ({cpu_count} cores, {cpu_freq:.2f}GHz)\n"
        f"🌡️ Temp: {cpu_temp}°C\n\n"
        
        f"🧠 RAM: {ram.percent}% ({get_size(ram.used)}/{get_size(ram.total)})\n"
        f"💾 Swap: {swap.percent}% ({get_size(swap.used)}/{get_size(swap.total)})\n\n"
        
        f"💽 Disk: {disk.percent}% ({get_size(disk.used)}/{get_size(disk.total)})\n"
        f"📊 IO: R {get_size(disk_io.read_bytes)} / W {get_size(disk_io.write_bytes)}\n\n"
        
        f"🌐 Net: ↑{get_size(net_io.bytes_sent)} ↓{get_size(net_io.bytes_recv)}\n"
        f"👾 Processes: {processes}"
    )
    
    stats_label.config(text=stats_text)
    stats_label.after(1000, update_stats)

# Настройка окна
root = tk.Tk()
root.title("Advanced System Monitor")
root.geometry("400x450+50+50")
root.attributes("-topmost", True)
root.config(bg="#222222")

# Стиль для текста
stats_label = tk.Label(
    root, 
    font=("Consolas", 10),
    bg="#222222", 
    fg="#00FF00",
    justify="left",
    padx=10,
    pady=10
)
stats_label.pack()

# Кнопка выхода
exit_button = tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    bg="#333333",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    bd=0
)
exit_button.pack(pady=5)

update_stats()
root.mainloop()