from vosk import Model, KaldiRecognizer
import pyaudio

class STTListener:
    def __init__(self, model_path="vosk-model-small-ru-0.22"):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        self.stream.start_stream()

    def listen_once(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data):
                result = self.rec.Result()
                return eval(result)["text"]