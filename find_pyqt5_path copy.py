import os
import sys

site_packages = r"C:\Users\Пользователь\AppData\Local\Programs\Python\Python313\Lib\site-packages"

print("🔍 Ищем qwindows.dll...")
print("=" * 60)

# Ищем qwindows.dll во всех подпапках site-packages
found = False
for root, dirs, files in os.walk(site_packages):
    if 'qwindows.dll' in files:
        dll_path = os.path.join(root, 'qwindows.dll')
        print(f"✅ Найден qwindows.dll: {dll_path}")
        
        # Определяем путь к папке plugins (родительский для platforms)
        platforms_path = os.path.dirname(dll_path)
        plugins_path = os.path.dirname(platforms_path)
        print(f"✅ Путь к плагинам: {plugins_path}")
        
        # Проверяем содержимое папки platforms
        print(f"Содержимое platforms: {os.listdir(platforms_path)}")
        found = True
        break

if not found:
    print("❌ qwindows.dll не найден!")
    print("\nПроверяем установленные пакеты:")
    
    # Проверяем все папки с PyQt5
    for item in os.listdir(site_packages):
        if 'pyqt5' in item.lower() or 'qt5' in item.lower():
            item_path = os.path.join(site_packages, item)
            if os.path.isdir(item_path):
                print(f"  - {item}")
                # Показываем содержимое
                try:
                    contents = os.listdir(item_path)[:5]
                    print(f"    Содержимое: {contents}")
                except:
                    pass