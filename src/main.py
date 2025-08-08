import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tray_icon import TrayIcon

if __name__ == "__main__":
    # Запускаем tray icon
    tray = TrayIcon()
    tray.run()