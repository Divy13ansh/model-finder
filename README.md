# FastAPI + Sketchfab Viewer

Minimal FastAPI backend with a CSR frontend that searches Sketchfab and loads the model with the Viewer API.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## API

- `GET /api/health`
- `GET /api/message`
- `GET /api/find-model?query=...`

## Env

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT` (defaults to `gpt-5.4-mini`)
- `SKETCHFAB_API_URL`
