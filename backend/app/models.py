from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    name: str = Field(..., min_length=1, description="Naziv agenta - ujedno i skill/tip tiketa kojeg pokriva")
    kapacitet: int = Field(..., ge=1)


class SimulationConfig(BaseModel):
    strategy: str = Field(..., description="Kljuc strategije, vidi GET /api/strategies")
    broj_tiketa: int = Field(200, ge=10, le=2000)
    duljina_tiketa: int = Field(6, ge = 3, le = 9)
    prosjecni_razmak: float = Field(0.8, ge=0.2, le=3.4)
    seed: int = Field(42, ge=0)
    tocnost_proxyja: float = Field(0.8, ge=0.0, le=1.0)
    proxy_kapacitet: int = Field(5, ge=1)
    postotak_urgent: float = Field(0.1, ge=0.0, le=1.0)
    odbacuj_pune: bool = False
    faktor_penala: float = Field(2.2, ge=1.0, le=5.0)
    agents: List[AgentConfig] = Field(..., min_length=1)
    tip_weights: Optional[Dict[str, float]] = None
    include_log: bool = False


class CompareConfig(BaseModel):
    strategies: Optional[list] = Field(None, description="Ako izostavljeno, uspoređuju se sve strategije")
    broj_tiketa: int = Field(200, ge=10, le=2000)
    duljina_tiketa: int = Field(6, ge = 3, le = 9)
    prosjecni_razmak: float = Field(0.8, ge=0.2, le=3.4)
    seed: int = Field(42, ge=0)
    tocnost_proxyja: float = Field(0.8, ge=0.0, le=1.0)
    proxy_kapacitet: int = Field(5, ge=1)
    postotak_urgent: float = Field(0.1, ge=0.0, le=1.0)
    odbacuj_pune: bool = False
    faktor_penala: float = Field(2.2, ge=1.0, le=5.0)
    agents: List[AgentConfig] = Field(..., min_length=1)
    tip_weights: Optional[Dict[str, float]] = None


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
    aktivni_tiketi: Optional[list] = None


class StrategyInfo(BaseModel):
    key: str
    label: str
