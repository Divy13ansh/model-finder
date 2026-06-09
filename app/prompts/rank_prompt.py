from prompts.base_prompt import BASE_PROMPT

RANK_PROMPT = BASE_PROMPT + """

The user is searching for:

QUERY:
{query}

You will be shown a thumbnail for a candidate model.

Evaluate how well this candidate matches the query.

Return ONLY valid JSON:

{
    "score": <integer from 0 to 100>,
    "reason": "<one short sentence>"
}

Scoring guide:

90-100:
Excellent match. Highly relevant, visually clear, educationally useful.

70-89:
Good match. Relevant but may have minor issues.

50-69:
Partially relevant. Usable but not ideal.

20-49:
Weak match. Significant relevance or quality issues.

0-19:
Poor match. Irrelevant or misleading.
"""