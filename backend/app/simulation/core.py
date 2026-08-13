"""
Jezgra simulacije viseagentskog sustava za korisnicku podrsku.
Cista logika, bez ispisa/CLI-ja - to radi runner.py koji ovo poziva
i vraca strukturirane rezultate API sloju.
"""

import random
import simpy
from dataclasses import dataclass, field
from enum import IntEnum


# ---------------------------------------------------------
# 1. MODEL PODATAKA
# ---------------------------------------------------------

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    URGENT = 0  # niza vrijednost = visi prioritet (simpy PriorityResource konvencija)


@dataclass
class Ticket:
    id: int
    tip: str            # STVARNI tip, npr. "tehnicki", "naplata", "opci"
    priority: Priority
    processing_time: float
    arrival_time: float
    # Popunjava ga ProxyAgent prije rasporedivanja. Samo PROCJENA tipa -
    # ne mora se poklapati sa stvarnim `tip`.
    predicted_tip: str = None


@dataclass
class Agent:
    name: str
    kapacitet: int
    skill: str           # tip upita za koji je agent najbrzi/specijaliziran
    trenutno_zauzet: int = 0

    @property
    def opterecenje(self):
        """Postotak iskoristenosti kapaciteta - koristi ga least-loaded strategija."""
        return self.trenutno_zauzet / self.kapacitet


# ---------------------------------------------------------
# 2. METRIKE
# ---------------------------------------------------------

@dataclass
class Metrike:
    vremena_cekanja: list = field(default_factory=list)
    vremena_odziva: list = field(default_factory=list)  # cekanje + obrada
    cekanje_po_prioritetu: dict = field(default_factory=lambda: {p: [] for p in Priority})
    odbaceni: int = 0
    log: list = field(default_factory=list)  # per-ticket zapisi za frontend

    def zabiljezi(self, ticket: Ticket, agent: Agent, start_obrade: float, kraj_obrade: float):
        cekanje = start_obrade - ticket.arrival_time
        odziv = kraj_obrade - ticket.arrival_time
        self.vremena_cekanja.append(cekanje)
        self.vremena_odziva.append(odziv)
        self.cekanje_po_prioritetu[ticket.priority].append(cekanje)
        self.log.append({
            "id": ticket.id,
            "tip": ticket.tip,
            "predicted_tip": ticket.predicted_tip,
            "priority": ticket.priority.name,
            "agent": agent.name,
            "arrival_time": round(ticket.arrival_time, 2),
            "cekanje": round(cekanje, 2),
            "odziv": round(odziv, 2),
        })

    def prosjecno_cekanje(self):
        return sum(self.vremena_cekanja) / len(self.vremena_cekanja) if self.vremena_cekanja else 0

    def prosjecan_odziv(self):
        return sum(self.vremena_odziva) / len(self.vremena_odziva) if self.vremena_odziva else 0

    def max_cekanje(self):
        return max(self.vremena_cekanja) if self.vremena_cekanja else 0

    def p95_cekanje(self):
        if not self.vremena_cekanja:
            return 0
        podaci = sorted(self.vremena_cekanja)
        idx = int(0.95 * len(podaci))
        return podaci[min(idx, len(podaci) - 1)]

    def prosjecno_cekanje_urgent(self):
        urgent = self.cekanje_po_prioritetu[Priority.URGENT]
        return sum(urgent) / len(urgent) if urgent else 0


# ---------------------------------------------------------
# 3. PROXY AGENT (KLASIFIKACIJA PRIJE RASPOREDIVANJA)
# ---------------------------------------------------------
# Simulira "prvi kontakt" koji na brzinu procjenjuje tip upita PRIJE nego
# se tiket proslijedi specijaliziranim agentima. Procjena ne mora biti
# tocna - strategije koje gledaju "skill" agenta odlucuju na temelju ove
# procjene, ne stvarnog tipa. Stvarni tip i dalje odreduje koliko obrada
# stvarno traje (vidi faktor u Scheduler.obradi_ticket).

class ProxyAgent:
    def __init__(self, tocnost: float = 0.8, moguci_tipovi: list = None, seed: int = None):
        self.tocnost = tocnost
        self.moguci_tipovi = moguci_tipovi or ["tehnicki", "naplata", "opci"]
        self.rng = random.Random(seed)  # zaseban RNG - ne remeti generiranje tiketa
        self.tocne_klasifikacije = 0
        self.pogresne_klasifikacije = 0

    def klasificiraj(self, ticket: Ticket) -> str:
        if self.rng.random() < self.tocnost:
            procjena = ticket.tip
            self.tocne_klasifikacije += 1
        else:
            ostali = [t for t in self.moguci_tipovi if t != ticket.tip]
            procjena = self.rng.choice(ostali)
            self.pogresne_klasifikacije += 1
        ticket.predicted_tip = procjena
        return procjena

    def stopa_tocnosti(self) -> float:
        ukupno = self.tocne_klasifikacije + self.pogresne_klasifikacije
        return self.tocne_klasifikacije / ukupno if ukupno else 0.0


# ---------------------------------------------------------
# 4. STRATEGIJE RASPOREDIVANJA
# ---------------------------------------------------------

def round_robin_strategy():
    zadnji_index = [-1]

    def strategija(ticket: Ticket, agenti: list) -> Agent:
        zadnji_index[0] = (zadnji_index[0] + 1) % len(agenti)
        return agenti[zadnji_index[0]]

    return strategija


def least_loaded_strategy(ticket: Ticket, agenti: list) -> Agent:
    return min(agenti, key=lambda a: a.opterecenje)


def skill_based_strategy(ticket: Ticket, agenti: list) -> Agent:
    procijenjeni_tip = ticket.predicted_tip if ticket.predicted_tip is not None else ticket.tip
    kandidati = [a for a in agenti if a.skill == procijenjeni_tip and a.opterecenje < 1.0]
    if kandidati:
        return min(kandidati, key=lambda a: a.opterecenje)
    return least_loaded_strategy(ticket, agenti)


def priority_least_loaded_strategy(ticket: Ticket, agenti: list) -> Agent:
    procijenjeni_tip = ticket.predicted_tip if ticket.predicted_tip is not None else ticket.tip
    if ticket.priority <= Priority.HIGH:
        skill_kandidati = [a for a in agenti if a.skill == procijenjeni_tip]
        if skill_kandidati:
            return min(skill_kandidati, key=lambda a: a.opterecenje)
    return least_loaded_strategy(ticket, agenti)


# Registar dostupnih strategija - jedini izvor istine, koristi ga i runner i API.
STRATEGY_REGISTRY = {
    "round_robin": {
        "label": "Round Robin",
        "factory": lambda: round_robin_strategy(),
    },
    "least_loaded": {
        "label": "Least Loaded",
        "factory": lambda: least_loaded_strategy,
    },
    "skill_based": {
        "label": "Skill Based",
        "factory": lambda: skill_based_strategy,
    },
    "hybrid": {
        "label": "ako je urgent/high onda skill_based, inace least_loaded",
        "factory": lambda: priority_least_loaded_strategy,
    },
}


# ---------------------------------------------------------
# 5. SCHEDULER
# ---------------------------------------------------------

class Scheduler:
    def __init__(self, env: simpy.Environment, agenti: list, strategija, metrike: Metrike, proxy: ProxyAgent):
        self.env = env
        self.agenti = agenti
        self.strategija = strategija
        self.metrike = metrike
        self.proxy = proxy

    def obradi_ticket(self, ticket: Ticket):
        self.proxy.klasificiraj(ticket)

        agent = self.strategija(ticket, self.agenti)

        while agent.trenutno_zauzet >= agent.kapacitet:
            yield self.env.timeout(0.1)
            agent = self.strategija(ticket, self.agenti)

        agent.trenutno_zauzet += 1
        start_obrade = self.env.now

        # brzina obrade ovisi o STVARNOM tipu (ticket.tip), ne o proxyjevoj
        # procjeni - pogresna procjena ne cini posao lakim, samo moze
        # poslati tiket agentu koji za njega nije specijaliziran.
        faktor = 1.0 if agent.skill == ticket.tip else 2.2
        yield self.env.timeout(ticket.processing_time * faktor)

        agent.trenutno_zauzet -= 1
        kraj_obrade = self.env.now
        self.metrike.zabiljezi(ticket, agent, start_obrade, kraj_obrade)


# ---------------------------------------------------------
# 6. GENERATOR ZAHTJEVA
# ---------------------------------------------------------

def generator_zahtjeva(
    env: simpy.Environment,
    scheduler: Scheduler,
    broj_tiketa: int,
    prosjecni_razmak: float,
    duljina_tiketa: float,
    tipovi: list,
    tip_weights: list,
):
    for i in range(broj_tiketa):
        yield env.timeout(random.expovariate(1.0 / prosjecni_razmak))  # Poisson dolasci
        ticket = Ticket(
            id=i,
            tip=random.choices(tipovi, weights=tip_weights)[0],
            priority=random.choices(
                list(Priority), weights=[0.4, 0.3, 0.2, 0.1]
            )[0],
            processing_time=random.uniform(duljina_tiketa - 2.9, duljina_tiketa + 3),
            arrival_time=env.now,
        )
        env.process(scheduler.obradi_ticket(ticket))


def build_agenti(agent_configs: list) -> list:
    return [
        Agent(name=c.name, kapacitet=c.kapacitet, skill=c.name)
        for c in agent_configs
    ]
