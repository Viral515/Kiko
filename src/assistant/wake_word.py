import pvporcupine
import pyaudio
import struct
import time

class WakeWordListener:
    def __init__(self, keyword_path, access_key):
        self.keyword_path = keyword_path
        self.access_key = access_key
        self.porcupine = None
        self.audio_stream = None
        self.pa = None

    def listen_for_wake_word(self):
        """Блокирующая функция: ждёт слово-активацию"""
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keyword_paths=[self.keyword_path]
            )

            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            print("👂 Слушаю... Скажи 'джарвис'")

            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    print("✅ Активирован!")
                    break
                time.sleep(0.01)
        except Exception as e:
            print(f"❌ Ошибка wake-word: {e}")
            return False
        finally:
            self.cleanup()
        return True

    def cleanup(self):
        if self.porcupine:
            self.porcupine.delete()
        if self.audio_stream:
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()