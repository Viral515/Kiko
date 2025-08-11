from assistant.stt import STTListener
from assistant.tts import TTSSpeaker
from assistant.commands import CommandManager
from assistant.llm import LLMClient
from assistant.wake_word import WakeWordListener
from dotenv import load_dotenv
from assistant.tools import TOOLS
import time
import gc
import os
import csv

load_dotenv()

class VoiceAssistant:
    def __init__(self, stt_model_path="vosk-model-small-ru-0.22"):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(current_dir, stt_model_path)
        
        print(f" Поиск модели Vosk: {model_path}")
        if not os.path.exists(model_path):
            print(f"❌ Модель не найдена: {model_path}")
            raise FileNotFoundError(f"Модель Vosk не найдена: {model_path}")

        access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        if not access_key:
            raise ValueError("❌ Не найден PORCUPINE_ACCESS_KEY в .env файле")

        wake_word_path = os.path.join(current_dir, "wake_words", "Jarvis_en_windows_v3_0_0.ppn")
        self.wake_word = WakeWordListener(keyword_path=wake_word_path, access_key=access_key)

        self.stt = STTListener(model_path=model_path)
        self.tts = TTSSpeaker()
        self.commands = CommandManager()
        self.llm = LLMClient(tools=TOOLS)
        self.listening_for_wake = True
        self.running = False

    def run(self):
        self.running = True
        self.tts.play_sound("goodMorning")
        while self.running:
            if self.wake_word.listen_for_wake_word():
                self.tts.play_sound("greet1")
                text = self.stt.listen_once()
                text = normalize_text(text)
                if text.strip():
                    print(f"Вы сказали: {text}")
                    cmd = self.commands.find_command(text)
                    if cmd:
                        self.commands.execute(cmd, self.tts)
                    else:
                        self.tts.play_sound("whatAreYouDoing")
                        #self.tts.speak("Думаю...")
                        #response = self.llm.generate(text)
                        #print("🤖 LLM: " + response)
                        #self.tts.speak(response)
            time.sleep(0.1)

    def stop(self):
            """Полная остановка и очистка всех ресурсов"""
            print("🛑 Начинаю остановку ассистента...")
            self.running = False

            # 1. Закрываем аудиоустройства
            if hasattr(self.stt, 'stream'):
                try:
                    self.stt.stream.stop_stream()
                    self.stt.stream.close()
                    print("✅ Аудиопоток STT закрыт")
                except Exception as e:
                    print(f"⚠️ Ошибка при закрытии STT stream: {e}")

            if hasattr(self.stt, 'p'):
                try:
                    self.stt.p.terminate()
                    print("✅ PyAudio завершён")
                except Exception as e:
                    print(f"⚠️ Ошибка при завершении PyAudio: {e}")

            # 2. Очищаем wake-word
            if hasattr(self, 'wake_word'):
                try:
                    self.wake_word.cleanup()
                    print("✅ Porcupine очищен")
                except Exception as e:
                    print(f"⚠️ Ошибка при очистке wake-word: {e}")

            # 3. Очищаем TTS (если нужно)
            # У TTSSpeaker нет активных потоков, но можно добавить cleanup при необходимости

            # 4. Явно удаляем объекты
            self.stt = None
            self.tts = None
            self.commands = None
            self.llm = None
            self.wake_word = None

            # 5. Принудительный сбор мусора
            gc.collect()
            print("✅ Ассистент остановлен и память очищена")

def load_word_replacements(csv_path):
    replacements = {}
    if not os.path.exists(csv_path):
        print(f"⚠️ Файл нормализации не найден: {csv_path}")
        return replacements

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=['wrong', 'correct'], delimiter=',', skipinitialspace=True)
            for row in reader:
                if row['wrong'].startswith('#') or row['wrong'].strip() == 'wrong':
                    continue
                replacements[row['wrong'].strip().lower()] = row['correct'].strip()
        print(f"✅ Загружено {len(replacements)} правил нормализации")
    except Exception as e:
        print(f"❌ Ошибка загрузки normalization.csv: {e}")
    return replacements

WORD_REPLACEMENTS = load_word_replacements(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "normalization.csv"))

def normalize_text(text):
    text = text.lower()
    for wrong, correct in WORD_REPLACEMENTS.items():
        if wrong in text:
            text = text.replace(wrong, correct)
    return text