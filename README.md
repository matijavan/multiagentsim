# Dispatch Sim — Ticket Routing Scheduler Comparison

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

Endpoints:
- `GET  /api/health` — liveness check
- `GET  /api/strategies` — list of available strategy keys/labels
- `POST /api/simulate` — run a single strategy, returns metrics (+ optional
  per-ticket log if `include_log: true`)
- `POST /api/compare` — run several strategies on the same seed (so ticket
  streams are identical) and return all results for direct comparison

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`. It talks to the backend at
`http://localhost:8000` by default — set `VITE_API_URL` in a `.env` file
in `frontend/` if you're running the backend elsewhere.

## Notes

- Both services must be running for the UI to work (start the backend
  first).
- `broj_tiketa` (ticket volume), `seed`, and `tocnost_proxyja` (proxy
  classifier accuracy) are all adjustable from the config panel, and the
  same seed is reused across strategies in a comparison run so the
  generated ticket stream is identical — differences you see are due to
  the routing strategy, not random variation in the input.
- This was built and syntax-checked in a sandboxed environment without
  outbound network access, so `pip install` / `npm install` could not be
  run end-to-end here — do that as the first step locally.
