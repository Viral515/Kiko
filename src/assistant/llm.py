import requests

class LLMClient:
    def __init__(self, base_url="http://127.0.0.1:8080", timeout=60):
        self.base_url = base_url
        self.timeout = timeout

    def generate(self, prompt, max_tokens=150):
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                timeout=self.timeout  # Теперь 60 секунд
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                return f"Ошибка LLM: {response.status_code}"
        except requests.exceptions.ReadTimeout:
            return "Извините, ответ занял слишком много времени."
        except Exception as e:
            return f"Не удалось подключиться к LLM: {e}"