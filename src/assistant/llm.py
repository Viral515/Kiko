import requests
import json

class LLMClient:
    def __init__(self, base_url="http://127.0.0.1:8080", tools=None):
        self.base_url = base_url
        self.tools = tools or {}

    def generate(self, prompt: str) -> str:
        """Генерирует ответ, обрабатывая вызовы инструментов"""
        try:
            # Отправляем запрос с описанием инструментов
            messages = [
                {
                    "role": "system",
                    "content": "You're Jarvis' voice assistant. You communicate exclusively in Russian. "
                             " You can perform actions through the tools."
                             "If you need to find or translate something, use the appropriate tool."
                             "Don't explain how you do it."
                },
                {"role": "user", "content": prompt}
            ]

            # Описание инструментов
            tools_spec = [
                {
                    "type": "function",
                    "function": {
                        "name": "search",
                        "description": "Search for information on the Internet",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"}
                            },
                            "required": ["query"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "translate",
                        "description": "Text translate",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string", "description": "Текст для перевода"},
                                "target_lang": {
                                    "type": "string",
                                    "description": "Целевой язык (en, de, fr, es, ru и др.)",
                                    "default": "en"
                                },
                                "source_lang": {
                                    "type": "string",
                                    "description": "Исходный язык (auto — автоматически)",
                                    "default": "auto"
                                }
                            },
                            "required": ["text"]
                        }
                    }
                }
            ]

            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "messages": messages,
                    "tools": tools_spec,
                    "tool_choice": "auto",
                    "max_tokens": 200
                },
                timeout=30
            )

            if response.status_code != 200:
                return f"Ошибка LLM: {response.status_code}"

            result = response.json()
            message = result["choices"][0]["message"]

            # Проверяем, вызван ли инструмент
            if "tool_calls" in message:
                tool_call = message["tool_calls"][0]
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])

                if tool_name in self.tools:
                    result = self.tools[tool_name](**tool_args)
                    return result
                else:
                    return f"Неизвестный инструмент: {tool_name}"
            else:
                return message["content"]

        except Exception as e:
            return f"Не удалось подключиться к LLM: {e}"