from assistant.stt import STTListener
from assistant.tts import TTSSpeaker
from assistant.commands import CommandManager
from assistant.llm import LLMClient

class VoiceAssistant:
    def __init__(self, stt_model_path="vosk-model-small-ru-0.22"):
        self.stt = STTListener(model_path=stt_model_path)
        self.tts = TTSSpeaker()
        self.commands = CommandManager()
        self.llm = LLMClient()
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
                    self.tts.play_sound("greet1")
                    self.listening_for_wake = False
            else:
                print(f"Вы сказали: {text}")
                cmd = self.commands.find_command(text)
                if cmd:
                    self.commands.execute(cmd, self.tts)
                else:
                    self.tts.speak("Думаю...")
                    response = self.llm.generate(text)
                    print("🤖 LLM: " + response)
                    self.tts.speak(response)
                print("🎙️ Ожидание команды... (скажите 'джарвис' снова)")
                self.listening_for_wake = True