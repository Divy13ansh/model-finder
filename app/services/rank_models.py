import math

def score(model):
    score = 0

    score += math.log10(model.get("viewCount", 0) + 1) * 10

    score += model.get("likeCount", 0) * 0.2

    score += model.get("downloadCount", 0) * 0.05

    if model.get("staffpickedAt"):
        score += 100

    if model.get("animationCount", 0) > 0:
        score += 50

    for category in model.get("categories", []):
        if category["name"] == "Science & Technology":
            score += 75

    return score


def rank_models(models):
    # Placeholder for ranking logic
    # For now, we simply return the first model as the best match
    if not models:
        return None
    for model in models:
        model["score"] = score(model)
    models.sort(key=lambda x: x["score"], reverse=True)

    return models[0] if models else None