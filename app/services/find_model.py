import requests
from app.services.rank_models import rank_models
import json
SEARCH_URL = "https://sketchfab.com/i/search"


def find_model(query: str):
    try:
        response = requests.get(
            SEARCH_URL,
            params={"q": query, "sort_by": "-relevance", "type": "models"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            models = data["results"]
            with open("models.json", "w") as f:
                json.dump(models, f, indent=4)
            model_info = rank_models(models)
            return {
                "name": model_info.get("name"),
                "uid": model_info.get("uid"),
            }
        return {"message": "No models found for the given query."}
    except Exception as e:
        return {"error": str(e)}
