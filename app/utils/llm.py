import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("LLM_API_URL")
MODEL = os.getenv("MODEL")

def query_llm(prompt: str, image_urls: list[str] | None = None):
    # Placeholder for LLM query logic
    # In a real implementation, this would call an LLM API like OpenAI's GPT-4

    content = []

    content.append({
        "type": "text",
        "text": prompt
    })

    if image_urls:
        for url in image_urls:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": url
                }
            })

    payload = {
        "model": MODEL,
        "messages": [{ "role": "user", "content": content }],
        "chat_template_kwargs": { "enable_thinking": True },
        "max_tokens": 16384,
        "stream": False,
        "temperature": 0.2,
        "top_p": 0.95
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    response.raise_for_status()

    data = response.json()
    # For demonstration, we'll return a mock response
    return {
        "model": MODEL,
        "response": data["choices"][0]["message"]["content"]
    }