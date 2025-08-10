from TTS.api import TTS
import pygame
import threading
import os

class TTSSpeaker:
    def __init__(self):
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sounds_dir = os.path.join(current_dir, "sounds")

    def speak(self, text):
        try:
            voice_sample_path = os.path.join(self.sounds_dir, "voiceSample", "JarvisVoiceSample.wav")
            temp_speech_path = os.path.join(os.path.dirname(self.sounds_dir), "temp_speech.wav")

            self.tts.tts_to_file(
                text=text,
                speaker_wav=voice_sample_path,
                language="ru",
                file_path=temp_speech_path
            )
            self._play_audio(temp_speech_path)
        except Exception as e:
            print(f"❌ Ошибка TTS: {e}")

    def play_sound(self, name):
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