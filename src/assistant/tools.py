import webbrowser
import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

def search(query: str) -> str:
    """Открывает поиск в браузере"""
    url = f"https://yandex.ru/search/?text={query}"
    webbrowser.open(url)
    return f"Ищу в Яндексе: {query}"


load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")

if not YANDEX_API_KEY:
    raise ValueError("❌ Не найден YANDEX_API_KEY в .env")
if not FOLDER_ID:
    raise ValueError("❌ Не найден FOLDER_ID в .env")


def translate_text(text: str, target_lang: str = "en", source_lang: str = "auto") -> str:
    """
    Переводит текст через Yandex Cloud Translate API
    """
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    payload = {
        "texts": [text],
        "targetLanguageCode": target_lang
    }
    if source_lang != "auto":
        payload["sourceLanguageCode"] = source_lang

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            translated = result["translations"][0]["text"]
            detected = result["translations"][0].get("detectedLanguageCode", "неизвестно")
            return f"Перевод: {translated} (распознан: {detected})"
        else:
            error = response.json().get("message", "неизвестная ошибка")
            return f"Ошибка перевода: {response.status_code} — {error}"
    except Exception as e:
        return f"Не удалось подключиться к Yandex Translate: {e}"

# Список инструментов
TOOLS = {
    "search": search,
    "translate": translate_text
}