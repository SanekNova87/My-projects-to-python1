import tkinter as tk

def click(button):
    current = display.get()
    
    if button == "=":
        try:
            result = eval(current)
            display.delete(0, tk.END)
            display.insert(0, str(result))
        except:
            display.delete(0, tk.END)
            display.insert(0, "Ошибка")
    
    elif button == "C":
        display.delete(0, tk.END)
        display.insert(0, "0")
    
    else:
        if current == "0":
            display.delete(0, tk.END)
        display.insert(tk.END, button)

# Создаем окно
root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x400")

# Поле для ввода
display = tk.Entry(root, font=("Arial", 20), justify="right")
display.pack(fill="x", padx=10, pady=10, ipady=10)
display.insert(0, "0")

# Кнопки
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+",
    "C"
]

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

row = 0
col = 0
for btn in buttons:
    b = tk.Button(frame, text=btn, font=("Arial", 14), width=5, height=2,
                  command=lambda x=btn: click(x))
    b.grid(row=row, column=col, padx=2, pady=2)
    col += 1
    if col > 3:
        col = 0
        row += 1

# ЭТА СТРОКА НУЖНА - ОНА ДЕРЖИТ ОКНО ОТКРЫТЫМ!
root.mainloop()