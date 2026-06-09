import os
import uuid
import requests


def download_thumbnail(url: str, save_dir: str = "thumbnails"):
    os.makedirs(save_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(save_dir, filename)

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=10,
    )

    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath