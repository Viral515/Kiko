import yaml
import os
import subprocess
import webbrowser
import sys
import random
from Levenshtein import ratio
import pyautogui
import psutil
import time

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
        """Находит команду с наилучшим совпадением"""
        text = text.lower().strip()
        best_match = None
        best_score = 0.0

        for cmd in self.commands:
            for trigger in cmd["triggers"]:

                # fuzzy-сравнение
                score = ratio(trigger, text)
                if score > best_score:
                    best_score = score
                    best_match = cmd

        # Порог: например, 0.7
        return best_match if best_score > 0.85 else None

    def get_random_response(self, cmd, response_type="tts"):
        """Возвращает случайный ответ из списка"""
        if "responses" not in cmd:
            return None

        responses = cmd["responses"].get(response_type, [])
        return random.choice(responses) if responses else None

    def execute(self, cmd, tts_speaker):
        action = cmd["action"]
        action_type = action["type"]
        target = action.get("target")
        args = action.get("args", [])

        print("Выполняется команда: " + action_type + " " + target)

        # --- Проигрываем ответ ---
        responses = cmd.get("responses", {})
        sound_list = responses.get("sound", [])
        tts_list = responses.get("tts", [])

        if sound_list:
            sound_name = random.choice(sound_list)
            tts_speaker.play_sound(sound_name)
        elif tts_list:
            tts_text = random.choice(tts_list)
            tts_speaker.speak(tts_text)

        if action_type == "script":
            self.run_script(target, args)
        elif action_type == "speak":
            print("Karma +1")
        elif action_type == "exit":
                sys.exit(0)



    def run_script(self, script_path, args):
        """Запускает внешний скрипт (PowerShell, CMD, Python)"""
        if not os.path.exists(script_path):
            print(f"❌ Скрипт не найден: {script_path}")
            return

        try:
            # Определяем, как запускать
            if script_path.endswith(".ps1"):
                # PowerShell
                subprocess.run([
                    "powershell", "-ExecutionPolicy", "Bypass", "-File", script_path
                ] + args, check=True, shell=True)
            elif script_path.endswith(".bat") or script_path.endswith(".cmd"):
                # CMD
                subprocess.run([script_path] + args, check=True, shell=True)
            elif script_path.endswith(".py"):
                # Python
                subprocess.run(["python", script_path] + args, check=True)
            else:
                print(f"❌ Неизвестный тип скрипта: {script_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка выполнения скрипта: {e}")