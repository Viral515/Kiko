import pystray
from PIL import Image, ImageDraw
import threading
import os
import sys
from assistant.core import VoiceAssistant

class TrayIcon:
    def __init__(self):
        self.assistant = None
        self.assistant_thread = None
        self.is_running = False
        self.icon = None
        
    def create_icon_image(self):
        """Создает простую иконку для трея"""
        # Создаем простое изображение 64x64 пикселей
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Рисуем простой круг с буквой K
        draw.ellipse([8, 8, 56, 56], fill=(0, 120, 215, 255), outline=(255, 255, 255, 255), width=2)
        draw.text((24, 20), "K", fill=(255, 255, 255, 255), font=None)
        
        return image
    
    def create_menu(self):
        """Создает контекстное меню"""
        return pystray.Menu(
            pystray.MenuItem("Запустить ассистента", self.start_assistant),
            pystray.MenuItem("Остановить ассистента", self.stop_assistant),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Настройки", self.open_settings),
            pystray.MenuItem("О программе", self.show_about),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Выход", self.quit_app)
        )
    
    def start_assistant(self, icon, item):
        """Запускает ассистента в отдельном потоке"""
        if not self.is_running:
            print("🔄 Запуск ассистента...")
            print(f" Текущая директория: {os.getcwd()}")
            try:
                self.is_running = True
                self.assistant = VoiceAssistant()
                self.assistant_thread = threading.Thread(target=self.run_assistant, daemon=True)
                self.assistant_thread.start()
                print("🎙️ Ассистент запущен в фоне")
            except Exception as e:
                print(f"❌ Ошибка запуска ассистента: {e}")
                self.is_running = False
    
    def stop_assistant(self, icon, item):
        """Останавливает ассистента"""
        if self.is_running:
            self.is_running = False
            if self.assistant:
                # Останавливаем ассистента
                self.assistant.stop()
            print("🛑 Ассистент остановлен")
    
    def run_assistant(self):
        """Запускает ассистента в фоновом режиме"""
        try:
            print("🎯 Запуск ассистента в фоновом режиме...")
            self.assistant.run()
        except Exception as e:
            print(f"❌ Ошибка в работе ассистента: {e}")
            import traceback
            traceback.print_exc()
            self.is_running = False
    
    def open_settings(self, icon, item):
        """Открывает настройки (пока заглушка)"""
        print("⚙️ Открытие настроек...")
        # TODO: Реализовать окно настроек
    
    def show_about(self, icon, item):
        """Показывает информацию о программе"""
        print("ℹ️ Kiko Voice Assistant v1.0")
        print("Голосовой ассистент для Windows")
    
    def quit_app(self, icon, item):
        """Выход из приложения"""
        self.stop_assistant(None, None)
        icon.stop()
        sys.exit(0)
    
    def run(self):
        """Запускает tray icon"""
        # Создаем иконку
        image = self.create_icon_image()
        menu = self.create_menu()
        
        self.icon = pystray.Icon(
            "kiko_assistant",
            image,
            "Kiko Voice Assistant",
            menu
        )
        
        print("🖥️ Tray icon запущен")
        self.icon.run()

if __name__ == "__main__":
    tray = TrayIcon()
    tray.run()
