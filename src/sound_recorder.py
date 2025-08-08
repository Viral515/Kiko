# test_xtts_russian.py
from TTS.api import TTS

print("Загружаю XTTS v2...")
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True, gpu=False)

print("Говорю на русском...")
tts.tts_to_file(
    text="Слушаю",
    file_path="sounds\listening5.wav",
    speaker_wav="14_out.wav",  # ✅ Используем проверенное имя
    language="ru"
)

print("✅ Аудио сохранено в russian_output.wav")