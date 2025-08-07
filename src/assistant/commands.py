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
        return best_match if best_score > 0.7 else None

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

        print("Выполняется команда: " + action_type + " " + target)

        # --- Выполняем действие ---
        if action_type == "run":
            subprocess.run(target, shell=True)

        elif action_type == "open_url":
            webbrowser.open(target.strip())

        elif action_type == "close":
            self.close_process(target)

        elif action_type == "key":
            self.send_keys(target)

        elif action_type == "exit":
            tts_speaker.speak("До свидания, сэр!")
            sys.exit(0)

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

    # --- Вспомогательные методы ---
    def close_process(self, process_name):
        """Закрывает процесс по имени (например, calc.exe)"""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                proc.kill()
                return

    def send_keys(self, keys):
        """Отправляет комбинацию клавиш, например 'ctrl+w'"""
        keys = keys.lower().split('+')
        keys = [k.strip() for k in keys]

        # Поддержка: ctrl, alt, shift, win
        mods = {
            'ctrl': 'ctrl',
            'alt': 'alt',
            'shift': 'shift',
            'win': 'win'
        }
        key = None
        args = []

        for k in keys:
            if k in mods:
                args.append(mods[k])
            else:
                key = k

        if key and args:
            pyautogui.hotkey(*args, key)
        elif key:
            pyautogui.press(key)