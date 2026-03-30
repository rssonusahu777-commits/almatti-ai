import os
import requests
from datetime import datetime
from dotenv import load_dotenv

class ChatAgent:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")

    def run(self, task: str) -> dict:
        print(f"[{self._ts()}] 🤖 Chat Agent running...")

        if not self.api_key:
            return {
                "status": "error",
                "agent": "ai_assistant",
                "response": "API key missing"
            }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "user", "content": task}
                    ]
                }
            )

            result = response.json()
            reply = result["choices"][0]["message"]["content"]

            return {
                "status": "success",
                "agent": "ai_assistant",
                "response": reply
            }

        except Exception as e:
            return {
                "status": "error",
                "agent": "ai_assistant",
                "response": str(e)
            }

    def _ts(self):
        return datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]