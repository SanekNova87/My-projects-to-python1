import os
import sys

print("=" * 60)
print("ПОИСК УСТАНОВКИ PyQt5")
print("=" * 60)

# Способ 1: Через импорт PyQt5
try:
    import PyQt5
    pyqt5_path = os.path.dirname(PyQt5.__file__)
    print(f"✓ PyQt5 найден по пути: {pyqt5_path}")
    
    # Ищем папку с плагинами
    possible_plugins = [
        os.path.join(pyqt5_path, 'Qt', 'plugins'),
        os.path.join(pyqt5_path, 'plugins'),
        os.path.join(pyqt5_path, 'PyQt5', 'Qt', 'plugins'),
    ]
    
    for path in possible_plugins:
        if os.path.exists(path):
            print(f"✓ Плагины найдены: {path}")
            print(f"\nСКОПИРУЙТЕ ЭТОТ ПУТЬ В КОД:")
            print(f'PLUGINS_PATH = r"{path}"')
            break
        else:
            print(f"✗ Папка не существует: {path}")
    
    # Проверяем наличие qwindows.dll
    platforms_path = os.path.join(pyqt5_path, 'Qt', 'plugins', 'platforms')
    if os.path.exists(platforms_path):
        dll_path = os.path.join(platforms_path, 'qwindows.dll')
        if os.path.exists(dll_path):
            print(f"✓ qwindows.dll найден: {dll_path}")
        else:
            print(f"✗ qwindows.dll не найден в {platforms_path}")
    
except ImportError:
    print("✗ PyQt5 НЕ УСТАНОВЛЕН!")

# Способ 2: Поиск через pip
print("\n" + "=" * 60)
print("ИНФОРМАЦИЯ ОБ УСТАНОВКЕ ЧЕРЕЗ PIP")
print("=" * 60)
import subprocess
try:
    result = subprocess.run([sys.executable, '-m', 'pip', 'show', 'PyQt5'], 
                          capture_output=True, text=True)
    print(result.stdout)
except:
    print("Не удалось получить информацию через pip")

# Способ 3: Где находится Python
print("\n" + "=" * 60)
print("ИНФОРМАЦИЯ О PYTHON")
print("=" * 60)
print(f"Путь к Python: {sys.executable}")
print(f"Папка Python: {sys.prefix}")
print(f"site-packages: {os.path.join(sys.prefix, 'Lib', 'site-packages')}")