# assistant/core.py
from assistant.stt import STTListener
from assistant.tts import TTSSpeaker
from assistant.commands import CommandManager

class VoiceAssistant:
    def __init__(self, stt_model_path="vosk-model-small-ru-0.22"):
        self.stt = STTListener(model_path=stt_model_path)
        self.tts = TTSSpeaker()
        self.commands = CommandManager()
        self.listening_for_wake = True

    def run(self):
        self.tts.play_sound("goodMorning")
        print("🎙️ Ассистент запущен. Скажи 'джарвис' для активации...")

        while True:
            text = self.stt.listen_once()

            if not text.strip():
                continue

            if self.listening_for_wake:
                if "джарвис" in text.lower():
                    print("✅ Активирован!")
                    self.tts.play_sound("greet1")  # Быстрый звук
                    self.listening_for_wake = False
            else:
                print(f"Вы сказали: {text}")
                cmd = self.commands.find_command(text)
                if cmd:
                    self.commands.execute(cmd, self.tts)
                else:
                    self.tts.speak("Не понял команду.")
                print("🎙️ Ожидание команды... (скажите 'джарвис' снова)")
                self.listening_for_wake = True