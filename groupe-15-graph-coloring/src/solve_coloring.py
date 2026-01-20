from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, List, Optional, Tuple
from ortools.sat.python import cp_model

Noeud = Hashable
Arete = Tuple[Noeud, Noeud]


@dataclass(frozen=True)
class InfosResolution:
    statut: str
    temps_s: float
    conflits: int
    branches: int


def _statut(s: int) -> str:
    return {cp_model.OPTIMAL: "OPTIMAL", cp_model.FEASIBLE: "FAISABLE",
            cp_model.INFEASIBLE: "IMPOSSIBLE"}.get(s, "INCONNU")


def _hint_glouton(noeuds: List[Noeud], aretes: List[Arete]) -> Dict[Noeud, int]:
    adj = {v: set() for v in noeuds}
    deg = {v: 0 for v in noeuds}
    for u, v in aretes:
        if u != v and u in adj and v in adj:
            adj[u].add(v); adj[v].add(u)
            deg[u] += 1; deg[v] += 1
    ordre = sorted(noeuds, key=lambda x: deg[x], reverse=True)
    col: Dict[Noeud, int] = {}
    for v in ordre:
        used = {col[u] for u in adj[v] if u in col}
        c = 0
        while c in used:
            c += 1
        col[v] = c
    return col


def solve_k_coloring(
    nodes: List[Noeud],
    edges: List[Arete],
    k: int,
    timeout_s: float = 5.0,
    symmetry_breaking: bool = True,
    num_workers: int = 8,
    use_hints: bool = True,
) -> Tuple[Optional[Dict[Noeud, int]], InfosResolution]:
    if k < 1:
        raise ValueError("k doit être >= 1")
    if not nodes:
        return {}, InfosResolution("OPTIMAL", 0.0, 0, 0)

    noeuds, aretes = list(nodes), list(edges)
    m = cp_model.CpModel()
    c = {v: m.NewIntVar(0, k - 1, f"c_{v}") for v in noeuds}

    if symmetry_breaking:
        m.Add(c[noeuds[0]] == 0)

    for u, v in aretes:
        if u != v and u in c and v in c:
            m.Add(c[u] != c[v])

    if use_hints:
        hint = _hint_glouton(noeuds, aretes)
        if max(hint.values(), default=-1) < k:
            for v, hv in hint.items():
                m.AddHint(c[v], int(hv))

    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = float(timeout_s)
    s.parameters.num_search_workers = int(num_workers)

    st = s.Solve(m)
    infos = InfosResolution(_statut(st), float(s.WallTime()), int(s.NumConflicts()), int(s.NumBranches()))

    if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return {v: int(s.Value(c[v])) for v in noeuds}, infos
    return None, infos


def solve_min_coloring(
    nodes: List[Noeud],
    edges: List[Arete],
    k_max: Optional[int] = None,
    timeout_per_k_s: float = 3.0,
    symmetry_breaking: bool = True,
    num_workers: int = 8,
) -> Tuple[Optional[int], Optional[Dict[Noeud, int]], List[Tuple[int, InfosResolution]]]:
    if not nodes:
        return 0, {}, []
    if k_max is None:
        k_max = len(nodes)

    journal: List[Tuple[int, InfosResolution]] = []
    for k in range(1, k_max + 1):
        sol, infos = solve_k_coloring(nodes, edges, k,
                                     timeout_s=timeout_per_k_s,
                                     symmetry_breaking=symmetry_breaking,
                                     num_workers=num_workers,
                                     use_hints=True)
        journal.append((k, infos))
        if sol is not None:
            return k, sol, journal
    return None, None, journal
