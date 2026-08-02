from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import CompareConfig, SimulationConfig, SimulationResult, StrategyInfo
from .simulation.core import STRATEGY_REGISTRY
from .simulation.runner import run_compare, run_simulation

app = FastAPI(
    title="Scheduler Simulation API",
    description="API za simulaciju rasporedivanja tiketa korisnicke podrske razlicitim strategijama.",
    version="1.0.0",
)

# Demo app - dopusti lokalni frontend dev server. Suzi origins u produkciji.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/strategies", response_model=list)
def list_strategies():
    return [{"key": key, "label": entry["label"]} for key, entry in STRATEGY_REGISTRY.items()]


@app.post("/api/simulate", response_model=SimulationResult)
def simulate(config: SimulationConfig):
    if config.strategy not in STRATEGY_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Nepoznata strategija: {config.strategy}")
    return run_simulation(
        strategy_key=config.strategy,
        broj_tiketa=config.broj_tiketa,
        seed=config.seed,
        tocnost_proxyja=config.tocnost_proxyja,
        include_log=config.include_log,
    )


@app.post("/api/compare", response_model=list)
def compare(config: CompareConfig):
    strategije = config.strategies or list(STRATEGY_REGISTRY.keys())
    nepoznate = [s for s in strategije if s not in STRATEGY_REGISTRY]
    if nepoznate:
        raise HTTPException(status_code=400, detail=f"Nepoznate strategije: {nepoznate}")
    return run_compare(
        strategy_keys=strategije,
        broj_tiketa=config.broj_tiketa,
        duljina_tiketa=config.duljina_tiketa,
        seed=config.seed,
        tocnost_proxyja=config.tocnost_proxyja,
    )
