from assistant.stt import STTListener
from assistant.tts import TTSSpeaker
from assistant.commands import CommandManager
from assistant.llm import LLMClient

import os

class VoiceAssistant:
    def __init__(self, stt_model_path="vosk-model-small-ru-0.22"):
        # Получаем абсолютный путь к модели
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(current_dir, stt_model_path)
        
        print(f"🔍 Поиск модели Vosk: {model_path}")
        if not os.path.exists(model_path):
            print(f"❌ Модель не найдена: {model_path}")
            raise FileNotFoundError(f"Модель Vosk не найдена: {model_path}")
        
        self.stt = STTListener(model_path=model_path)
        self.tts = TTSSpeaker()
        self.commands = CommandManager()
        self.llm = LLMClient()
        self.listening_for_wake = True
        self.running = False

    def run(self):
        """Обычный режим работы (консольный)"""
        self.running = True
        self.tts.play_sound("goodMorning")
        print("🎙️ Ассистент запущен. Скажи 'джарвис' для активации...")

        while self.running:
            text = self.stt.listen_once()

            if not text.strip():
                continue

            if self.listening_for_wake:
                if "джарвис" in text.lower():
                    print("✅ Активирован!")
                    self.tts.play_sound("greet1")
                    self.listening_for_wake = False
            else:
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
                print("🎙️ Ожидание команды... (скажите 'джарвис' снова)")
                self.listening_for_wake = True

    def run_background(self):
        """Фоновый режим работы (без консольного вывода)"""
        self.running = True
        self.tts.play_sound("goodMorning")
        
        while self.running:
            text = self.stt.listen_once()

            if not text.strip():
                continue

            if self.listening_for_wake:
                if "джарвис" in text.lower():
                    self.tts.play_sound("greet1")
                    self.listening_for_wake = False
            else:
                cmd = self.commands.find_command(text)
                if cmd:
                    self.commands.execute(cmd, self.tts)
                else:
                    self.tts.play_sound("whatAreYouDoing")
                    #self.tts.speak("Думаю...")
                    #response = self.llm.generate(text)
                    #self.tts.speak(response)
                self.listening_for_wake = True

    def stop(self):
        """Останавливает работу ассистента"""
        self.running = False
        if hasattr(self.stt, 'stream'):
            self.stt.stream.stop_stream()
            self.stt.stream.close()
        if hasattr(self.stt, 'p'):
            self.stt.p.terminate()