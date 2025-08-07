# assistant/commands.py
import yaml
import os
import subprocess
import webbrowser
import sys
import random
from Levenshtein import ratio

class CommandManager:
    def __init__(self, commands_file="commands/commands.yaml"):
        self.commands = []
        self.load_commands(commands_file)

    def load_commands(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл команд не найден: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            self.commands = yaml.safe_load(f)

    def find_command(self, text):
        """Находит команду по тексту (с нечётким сравнением)"""
        text = text.lower().strip()
        for cmd in self.commands:
            if any(self.fuzz_match(trigger, text) for trigger in cmd["triggers"]):
                return cmd
        return None

    def get_random_response(self, cmd, response_type="tts"):
        """Возвращает случайный ответ из списка"""
        if "responses" not in cmd:
            return None

        responses = cmd["responses"].get(response_type, [])
        return random.choice(responses) if responses else None

    def execute(self, cmd, tts_speaker):
        """Выполняет действие команды и проигрывает ответ"""
        # 1. Выполняем действие
        action = cmd["action"]
        action_type = action["type"]

        if action_type == "run":
            subprocess.run(action["target"], shell=True)
        elif action_type == "open_url":
            webbrowser.open(action["target"].strip())
        elif action_type == "exit":
            tts_speaker.speak("До свидания, сэр!")
            sys.exit(0)

        # 2. Проигрываем ответ: сначала sound, потом tts
        responses = cmd.get("responses", {})
        sound_list = responses.get("sound", [])
        tts_list = responses.get("tts", [])

        # Если есть звуки — играем случайный
        if sound_list:
            sound_name = random.choice(sound_list)
            tts_speaker.play_sound(sound_name)
        # Если нет звуков, но есть TTS — говорим
        elif tts_list:
            tts_text = random.choice(tts_list)
            tts_speaker.speak(tts_text)
        # Если вообще нет ответов — можно добавить дефолт
        else:
            tts_speaker.speak("Выполнено.")

    def fuzz_match(self, trigger, text, threshold=0.8):
        """
        Проверяет, насколько текст похож на триггер.
        threshold: 0.8 = 80% схожести
        """
        # Сначала пробуем обычное вхождение (быстро)
        if trigger in text:
            return True
        # Если не нашли — используем fuzzy-сравнение
        return ratio(trigger, text) > threshold