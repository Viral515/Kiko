#!/usr/bin/env python3
"""
Скрипт для установки зависимостей Kiko Voice Assistant
"""

import subprocess
import sys
import os
import platform

def install_pyaudio():
    """Устанавливает PyAudio с использованием pipwin или альтернативных источников"""
    try:
        print("🔧 Установка PyAudio...")
        
        # Сначала пробуем установить pipwin
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
            print("✅ pipwin установлен")
        except:
            print("⚠️ pipwin не установлен, пробуем альтернативные методы")
        
        # Пробуем установить через pipwin
        try:
            subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
            print("✅ PyAudio установлен через pipwin")
            return True
        except:
            print("⚠️ pipwin не сработал, пробуем прямой URL")
        
        # Пробуем установить через прямой URL
        try:
            python_version = f"{sys.version_info.major}{sys.version_info.minor}"
            architecture = "win_amd64" if platform.architecture()[0] == "64bit" else "win32"
            url = f"https://www.lfd.uci.edu/~gohlke/pythonlibs/PyAudio-0.2.11-cp{python_version}-cp{python_version}-{architecture}.whl"
            subprocess.check_call([sys.executable, "-m", "pip", "install", url])
            print("✅ PyAudio установлен через прямой URL")
            return True
        except:
            print("⚠️ Прямой URL не сработал")
        
        # Последняя попытка - обычная установка
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            print("✅ PyAudio установлен обычным способом")
            return True
        except:
            print("❌ Не удалось установить PyAudio")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка установки PyAudio: {e}")
        return False

def install_requirements():
    """Устанавливает зависимости из requirements.txt"""
    try:
        print("📦 Установка основных зависимостей...")
        
        # Создаем временный requirements без PyAudio
        temp_requirements = []
        with open("requirements.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "pyaudio" not in line.lower():
                    temp_requirements.append(line)
        
        # Записываем временный файл
        with open("temp_requirements.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(temp_requirements))
        
        # Устанавливаем зависимости без PyAudio
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "temp_requirements.txt"])
        print("✅ Основные зависимости установлены")
        
        # Устанавливаем PyAudio отдельно
        if install_pyaudio():
            print("✅ Все зависимости установлены успешно!")
            return True
        else:
            print("⚠️ PyAudio не установлен, но остальные зависимости работают")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки зависимостей: {e}")
        return False
    finally:
        # Удаляем временный файл
        if os.path.exists("temp_requirements.txt"):
            os.remove("temp_requirements.txt")

def check_vosk_model():
    """Проверяет наличие модели Vosk"""
    model_path = "src/vosk-model-small-ru-0.22"
    if not os.path.exists(model_path):
        print("⚠️ Модель Vosk не найдена!")
        print("Скачайте модель с https://alphacephei.com/vosk/models")
        print(f"И распакуйте в папку: {model_path}")
        return False
    print("✅ Модель Vosk найдена")
    return True

def test_imports():
    """Тестирует импорт основных модулей"""
    print("🧪 Тестирование импортов...")
    
    try:
        import vosk
        print("✅ vosk импортирован")
    except ImportError:
        print("❌ vosk не импортируется")
        return False
    
    try:
        import pyaudio
        print("✅ pyaudio импортирован")
    except ImportError:
        print("❌ pyaudio не импортируется")
        return False
    
    try:
        import pygame
        print("✅ pygame импортирован")
    except ImportError:
        print("❌ pygame не импортируется")
        return False
    
    try:
        import yaml
        print("✅ yaml импортирован")
    except ImportError:
        print("❌ yaml не импортируется")
        return False
    
    try:
        import pystray
        print("✅ pystray импортирован")
    except ImportError:
        print("❌ pystray не импортируется")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Установка Kiko Voice Assistant")
    print("=" * 50)
    
    if install_requirements():
        if test_imports():
            check_vosk_model()
            print("\n🎉 Установка завершена успешно!")
            print("Для запуска используйте: python src/main.py")
        else:
            print("\n⚠️ Установка завершена с предупреждениями")
            print("Некоторые модули могут не работать корректно")
    else:
        print("\n❌ Установка не удалась!")
        print("\n💡 Альтернативные решения:")
        print("1. Установите Visual Studio Build Tools")
        print("2. Попробуйте: pip install pipwin && pipwin install pyaudio")
        print("3. Скачайте PyAudio wheel файл вручную")
