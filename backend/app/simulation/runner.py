"""
Orkestrira jedno pokretanje simulacije (simpy env + scheduler + generator)
i vraca obican dict s rezultatima - bez ispisa, bez ovisnosti o API sloju.
"""

import random
import simpy

from .core import (
    STRATEGY_REGISTRY,
    Metrike,
    ProxyAgent,
    Scheduler,
    build_agenti,
    generator_zahtjeva,
)



def run_simulation(
    strategy_key: str,
    agents: list,
    broj_tiketa: int = 200,
    seed: int = 42,
    tocnost_proxyja: float = 0.8,
    include_log: bool = False,
    prosjecni_razmak: float = 0.8,
    duljina_tiketa: float = 5,
    tip_weights: dict = None,
    proxy_kapacitet: int = 5,
    postotak_urgent: float = 0.1,
) -> dict:
    if strategy_key not in STRATEGY_REGISTRY:
        raise ValueError(f"Nepoznata strategija: {strategy_key}")

    entry = STRATEGY_REGISTRY[strategy_key]
    strategija = entry["factory"]()  # svjeza instanca (round robin ima interno stanje)

    # Distinct tipovi tiketa = distinct nazivi/skillovi trenutno konfiguriranih
    # agenata (redoslijed prvog pojavljivanja), s tezinama iz tip_weights
    # (nedostajuci unosi padaju na 1.0 - ravnomjerna tezina).
    tipovi = list(dict.fromkeys(a.name for a in agents))
    tezine = tip_weights or {}
    tip_weights_list = [tezine.get(t, 1.0) for t in tipovi]
    priority_weights = [postotak_urgent, 1 - postotak_urgent]  # [URGENT, NORMAL]

    random.seed(seed)
    env = simpy.Environment()
    agenti = build_agenti(agents)
    metrike = Metrike()
    # Zaseban seed za proxy RNG - generiranje tiketa ostaje identicno bez
    # obzira na tocnost proxyja, pa je usporedba strategija fer.
    proxy = ProxyAgent(tocnost=tocnost_proxyja, moguci_tipovi=tipovi, seed=seed + 1000, kapacitet=proxy_kapacitet)
    scheduler = Scheduler(env, agenti, strategija, metrike, proxy)

    env.process(generator_zahtjeva(
        env, scheduler, broj_tiketa, prosjecni_razmak, duljina_tiketa, tipovi, tip_weights_list, priority_weights,
    ))
    env.run()

    ukupno_klasificirano = proxy.tocne_klasifikacije + proxy.pogresne_klasifikacije

    rezultat = {
        "strategy": strategy_key,
        "label": entry["label"],
        "prosjecno_cekanje": round(metrike.prosjecno_cekanje(), 3),
        "prosjecan_odziv": round(metrike.prosjecan_odziv(), 3),
        "max_cekanje": round(metrike.max_cekanje(), 3),
        "p95_cekanje": round(metrike.p95_cekanje(), 3),
        "prosjecno_cekanje_urgent": round(metrike.prosjecno_cekanje_urgent(), 3),
        "proxy_tocnost": round(proxy.stopa_tocnosti(), 4),
        "proxy_tocne": proxy.tocne_klasifikacije,
        "proxy_ukupno": ukupno_klasificirano,
        "odbaceni": metrike.odbaceni,
        "broj_tiketa_obradeno": len(metrike.vremena_cekanja),
        "ticket_log": metrike.log if include_log else None,
        "aktivni_tiketi": metrike.aktivni_po_ticku(),
    }
    return rezultat


def run_compare(
    strategy_keys: list,
    agents: list,
    broj_tiketa: int = 200,
    seed: int = 42,
    tocnost_proxyja: float = 0.8,
    prosjecni_razmak: float = 0.8,
    duljina_tiketa: float = 6,
    tip_weights: dict = None,
    proxy_kapacitet: int = 5,
    postotak_urgent: float = 0.1,
) -> list:
    """Pokrece vise strategija na ISTOM seedu (=> identicna simulacija), tako da su
    rezultati direktno usporedivi."""
    return [
        run_simulation(
            key,
            agents=agents,
            broj_tiketa=broj_tiketa,
            duljina_tiketa=duljina_tiketa,
            seed=seed,
            tocnost_proxyja=tocnost_proxyja,
            prosjecni_razmak=prosjecni_razmak,
            tip_weights=tip_weights,
            proxy_kapacitet=proxy_kapacitet,
            postotak_urgent=postotak_urgent,
        )
        for key in strategy_keys
    ]
