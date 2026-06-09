from app.prompts.rank_prompt import build_rank_prompt as RANK_PROMPT
from app.utils.llm import query_llm
from app.utils.thumbnail import download_thumbnail
import re

import json

def agent_model_rank(query, models):
    if not models:
        return None
    
    best_model = None
    best_score = -1

    for model in models:
        try:
            thumbnail_images = model.get("thumbnails", {}).get("images", [])
            if not thumbnail_images:
                raise ValueError("No thumbnail images available")

            thumbnail_index = min(3, len(thumbnail_images) - 1)
            thumbnail_url = thumbnail_images[thumbnail_index]["url"]

            prompt = RANK_PROMPT(query=query)

            thumbnail_path = download_thumbnail(thumbnail_url)

            response = query_llm(
                prompt,
                image_paths=[thumbnail_path]
            )

            
            print(f"LLM response for model {model.get('name', 'Unknown')}: {response['response']}")

            match = re.search(r"\{.*\}", response["response"], re.DOTALL)

            if not match:
                raise ValueError("No JSON found")

            result = json.loads(match.group())

            score = int(result.get("score", 0))

            if score > best_score:
                best_score = score
                best_model = model
                print(f"Model: {model.get('name', 'Unknown')}, Score: {score}")

        except Exception as e:
            print(
                f"Error processing model {model.get('name', 'Unknown')}: {e}"
            )


    if not best_model:
        return None
    return best_model, best_score
