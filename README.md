# Model Finder

Model Finder is a FastAPI app with a plain CSR frontend that searches Sketchfab models, ranks thumbnails with Azure OpenAI, and loads the selected result in the Sketchfab Viewer API.

## Overview

The app is split into three parts:

- a FastAPI backend for search and ranking
- a static HTML/CSS/JS frontend
- the Sketchfab Viewer embedded in an iframe

The backend searches Sketchfab, downloads candidate thumbnails, sends them to Azure OpenAI, and returns the best match to the browser.

## Features

- Sketchfab model search API
- thumbnail ranking with Azure OpenAI `gpt-5.4-mini`
- CSR frontend with no templates or Jinja
- Sketchfab Viewer API integration
- simple API health endpoints

## Project Structure

```text
app/
  main.py                 FastAPI entrypoint
  services/
    find_model.py         Search + ranking orchestration
    agent_model_rank.py    LLM-based thumbnail ranking
    rank_models.py         Local heuristic ranking helper
  utils/
    llm.py                Azure OpenAI wrapper
    thumbnail.py          Thumbnail download helper
  prompts/
    base_prompt.py        Ranking instructions
    rank_prompt.py        Query-specific prompt builder
  static/
    index.html            CSR shell
    app.js                Frontend logic
    styles.css            Basic styling
thumbnails/               Downloaded model thumbnails
.env                      Local secrets and config
```

## Tech Stack

- FastAPI
- Python 3.13+
- Plain HTML, CSS, and JavaScript
- Sketchfab Viewer API
- Azure OpenAI

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you already have `.venv`, just activate it and reinstall if needed:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
SKETCHFAB_API_URL=https://sketchfab.com/i/search
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/v1/
AZURE_OPENAI_DEPLOYMENT=gpt-5.4-mini
```

### Variable Details

- `SKETCHFAB_API_URL`: Sketchfab search endpoint used by the backend
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint including `/openai/v1/`
- `AZURE_OPENAI_DEPLOYMENT`: model deployment name, defaults to `gpt-5.4-mini`

## Run

Start the app with Uvicorn:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## API Endpoints

- `GET /api/health` returns `{"status": "ok"}`
- `GET /api/message` returns a simple backend status message
- `GET /api/find-model?query=...` searches Sketchfab and returns the best ranked model

## Request Flow

1. The user enters a search query in the frontend.
2. The browser calls `/api/find-model`.
3. `find_model.py` queries Sketchfab for candidate models.
4. The top results are sent to `agent_model_rank.py`.
5. Each candidate thumbnail is downloaded locally.
6. `utils/llm.py` sends the thumbnail and prompt to Azure OpenAI.
7. The best-scoring model is returned to the frontend.
8. The frontend loads the model in the Sketchfab Viewer iframe.

## Ranking Logic

Ranking happens in two stages:

1. `rank_models.py` contains a lightweight heuristic scorer for local ranking.
2. `agent_model_rank.py` uses Azure OpenAI to score thumbnail relevance with a JSON response contract.

The model is expected to return JSON in this format:

```json
{
  "score": 87,
  "reason": "Highly relevant thumbnail for the query"
}
```

## Frontend Notes

- The frontend is static HTML, not a React/Vue app.
- It uses `fetch()` to call the backend API.
- The Sketchfab Viewer API script is loaded from Sketchfab’s CDN.
- The iframe includes the required permissions and sandbox flags.

## Development Notes

- Downloaded thumbnails are stored in `thumbnails/`.
- `.env` is ignored by git, so secrets stay local.
- The app expects the Azure deployment to support image input.
- If the Azure API returns rate-limit errors, reduce the number of candidates ranked per query.

## Troubleshooting

### Missing Azure credentials

If you see a missing credentials error, check that `.env` contains:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`

### No models found

If search returns no results, verify `SKETCHFAB_API_URL` and the query text.

### Viewer does not load

Make sure the model UID is valid and that Sketchfab allows embedding for the model.

### Rate limits

If Azure OpenAI is rate-limiting you, lower the number of ranked candidates or add retries.

## Next Improvements

- add retry/backoff for Azure OpenAI errors
- cache model rankings by query
- expose ranked candidates in the UI
- move backend routes into separate router modules
