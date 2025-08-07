from TTS.api import TTS
import pygame
import threading
import os

class TTSSpeaker:
    def __init__(self):
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        self.sounds_dir = "sounds"

    def speak(self, text):
        """Озвучивает текст через TTS"""
        def _run():
            try:
                self.tts.tts_to_file(
                    text=text,
                    speaker_wav="sounds/voiceSample/JarvisVoiceSample.wav",
                    language="ru",
                    file_path="temp_speech.wav"
                )
                self._play_audio("temp_speech.wav")
            except Exception as e:
                print(f"❌ Ошибка TTS: {e}")

        thread = threading.Thread(target=_run)
        thread.start()

    def play_sound(self, name):
        """Мгновенно проигрывает звук из папки sounds"""
        try:
            sound_file = os.path.join(self.sounds_dir, f"{name}.wav")
            if os.path.exists(sound_file):
                self._play_audio(sound_file)
        except Exception as e:
            print(f"❌ Ошибка воспроизведения звука: {e}")

    def _play_audio(self, file_path):
        """Проигрывает аудиофайл"""
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()