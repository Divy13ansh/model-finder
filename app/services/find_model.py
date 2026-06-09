import requests
from app.services.agent_model_rank import agent_model_rank
import os
from dotenv import load_dotenv
load_dotenv()

SEARCH_URL = os.getenv("SKETCHFAB_API_URL")
def find_model(query: str):
    try:
        response = requests.get(
            SEARCH_URL,
            params={
                "q": query,
                "sort_by": "-relevance",
                "type": "models"
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return {
                "message": "No models found."
            }

        candidates = results[:5]

        ranked = agent_model_rank(
            query=query,
            models=candidates
        )

        if not ranked:
            return {
                "message": "No suitable model found."
            }

        best_model, best_score = ranked

        return {
            "name": best_model.get("name"),
            "uid": best_model.get("uid"),
            "embedUrl": best_model.get("embedUrl"),
            "viewerUrl": best_model.get("viewerUrl"),
            "score": best_score,
        }

    except Exception as e:
        return {
            "error": str(e)
        }
