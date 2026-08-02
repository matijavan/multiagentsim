from typing import Optional
from pydantic import BaseModel, Field


class SimulationConfig(BaseModel):
    strategy: str = Field(..., description="Kljuc strategije, vidi GET /api/strategies")
    broj_tiketa: int = Field(200, ge=10, le=2000)
    duljina_tiketa: int = Field(6, ge = 3, le = 9)
    seed: int = Field(42, ge=0)
    tocnost_proxyja: float = Field(0.8, ge=0.0, le=1.0)
    include_log: bool = False


class CompareConfig(BaseModel):
    strategies: Optional[list] = Field(None, description="Ako izostavljeno, uspoređuju se sve strategije")
    broj_tiketa: int = Field(200, ge=10, le=2000)
    duljina_tiketa: int = Field(6, ge = 3, le = 9)
    seed: int = Field(42, ge=0)
    tocnost_proxyja: float = Field(0.8, ge=0.0, le=1.0)


class TicketLogEntry(BaseModel):
    id: int
    tip: str
    predicted_tip: Optional[str]
    priority: str
    agent: str
    arrival_time: float
    cekanje: float
    odziv: float


class SimulationResult(BaseModel):
    strategy: str
    label: str
    prosjecno_cekanje: float
    prosjecan_odziv: float
    max_cekanje: float
    p95_cekanje: float
    prosjecno_cekanje_urgent: float
    proxy_tocnost: float
    proxy_tocne: int
    proxy_ukupno: int
    odbaceni: int
    broj_tiketa_obradeno: int
    ticket_log: Optional[list] = None


class StrategyInfo(BaseModel):
    key: str
    label: str
