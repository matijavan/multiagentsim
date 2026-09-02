# Multi-agent scheduler simulator

A small fullstack app around the `simpy`-based multi-agent ticket scheduling
simulation: a FastAPI backend runs the simulation on demand, a React
frontend lets you configure a run and compares strategies side by side.

```
backend/     FastAPI app wrapping the simulation (app/simulation/core.py, runner.py)
frontend/    React + Vite app (config panel, charts, table)
```

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be at `http://localhost:8000`. Interactive docs (Swagger UI)
are auto-generated at `http://localhost:8000/docs`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`. It talks to the backend at
`http://localhost:8000` by default — set `VITE_API_URL` in a `.env` file
in `frontend/` if you're running the backend elsewhere.