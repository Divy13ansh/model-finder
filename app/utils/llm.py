import base64
import mimetypes
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.4-mini")

client = OpenAI(base_url=ENDPOINT, api_key=API_KEY)


def _image_to_data_uri(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    mime_type = mime_type or "image/jpeg"

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def query_llm(prompt: str, image_paths: list[str] | None = None):
    content = [{"type": "text", "text": prompt}]

    if image_paths:
        for image_path in image_paths:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": _image_to_data_uri(image_path)},
                }
            )

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    return {
        "model": DEPLOYMENT,
        "response": response.choices[0].message.content or "",
    }
