import yaml
import os
import subprocess
import sys
import random
from Levenshtein import ratio
import glob

class CommandManager:
    def __init__(self, commands_dir="commands"):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        commands_path = os.path.join(current_dir, commands_dir)
        
        print(f"Загрузка команд из: {commands_path}")
        self.commands = []
        self.load_all_commands(commands_path)

    def load_all_commands(self, commands_dir):
        if not os.path.exists(commands_dir):
            raise FileNotFoundError(f"Папка команд не найдена: {commands_dir}")

        yaml_files = glob.glob(os.path.join(commands_dir, "*.yaml"))
        
        if not yaml_files:
            raise FileNotFoundError(f"YAML файлы не найдены в папке: {commands_dir}")

        print(f"Загружаю команды из {len(yaml_files)} файлов...")
        
        for yaml_file in yaml_files:
            try:
                print(f"Загружаю: {os.path.basename(yaml_file)}")
                with open(yaml_file, "r", encoding="utf-8") as f:
                    file_commands = yaml.safe_load(f)
                    if file_commands:
                        self.commands.extend(file_commands)
                        print(f"  Загружено {len(file_commands)} команд")
            except Exception as e:
                print(f"❌ Ошибка загрузки {yaml_file}: {e}")

        print(f"Всего загружено команд: {len(self.commands)}")

    def find_command(self, text):
        text = text.lower().strip()
        best_match = None
        best_score = 0.0

        for cmd in self.commands:
            for trigger in cmd["triggers"]:
                score = ratio(trigger, text)
                if score > best_score:
                    best_score = score
                    best_match = cmd

        return best_match if best_score > 0.85 else None

    def get_random_response(self, cmd, response_type="tts"):
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

    def run_script(self, script_path, args):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        absolute_script_path = os.path.join(current_dir, script_path)
        
        print(f" Выполнение скрипта: {absolute_script_path}")
        
        if not os.path.exists(absolute_script_path):
            print(f"❌ Скрипт не найден: {absolute_script_path}")
            return

        try:
            if script_path.endswith(".ps1"):
                subprocess.run([
                    "powershell", "-ExecutionPolicy", "Bypass", "-File", absolute_script_path
                ] + args, check=True, shell=True)
            elif script_path.endswith(".bat") or script_path.endswith(".cmd"):
                subprocess.run([absolute_script_path] + args, check=True, shell=True)
            elif script_path.endswith(".py"):
                subprocess.run(["python", absolute_script_path] + args, check=True)
            else:
                print(f"❌ Неизвестный тип скрипта: {absolute_script_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка выполнения скрипта: {e}")
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")