from assistant.stt import STTListener
from assistant.tts import TTSSpeaker
from assistant.commands import CommandManager
from assistant.llm import LLMClient
from assistant.wake_word import WakeWordListener
from dotenv import load_dotenv
import time

import os

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
        self.llm = LLMClient()
        self.listening_for_wake = True
        self.running = False

    def run(self):
        """Обычный режим работы"""
        self.running = True
        self.tts.play_sound("goodMorning")
        print("🎙️ Ассистент запущен. Скажи 'джарвис' для активации...")

        while self.running:
            if self.wake_word.listen_for_wake_word():
                self.tts.play_sound("greet1")
                text = self.stt.listen_once()
                if text.strip():
                    print(f"Вы сказали: {text}")
                    cmd = self.commands.find_command(text)
                    if cmd:
                        self.commands.execute(cmd, self.tts)
                    else:
                        self.tts.play_sound("whatAreYouDoing")
                        # self.tts.speak("Думаю...")
                        # response = self.llm.generate(text)
                        # print("🤖 LLM: " + response)
                        # self.tts.speak(response)
                print("🎙️ Ожидание команды... (скажите 'джарвис' снова)")
            else:
                print("⚠️ Ошибка активации, продолжаю...")

    def run_background(self):
        """Фоновый режим"""
        self.running = True
        self.tts.play_sound("goodMorning")
        while self.running:
            if self.wake_word.listen_for_wake_word():
                self.tts.play_sound("greet1")
                text = self.stt.listen_once()
                if text.strip():
                    cmd = self.commands.find_command(text)
                    if cmd:
                        self.commands.execute(cmd, self.tts)
                    else:
                        self.tts.play_sound("whatAreYouDoing")
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if hasattr(self.stt, 'stream'):
            self.stt.stream.stop_stream()
            self.stt.stream.close()
        if hasattr(self.stt, 'p'):
            self.stt.p.terminate()
        if hasattr(self, 'wake_word'):
            self.wake_word.cleanup()