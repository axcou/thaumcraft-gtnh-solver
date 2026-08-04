"""Aspect-to-aspect connection helper.

Mirrors ythri/tcresearch's linker: given two aspects, find the cheapest walk
between them in the combination graph (revisiting aspects is allowed) that
is at least `min_steps` hops long -- Thaumcraft only lets you link two
research-table aspects directly when they are far enough apart in the
combination graph, so a same-length shortcut is not always usable.

Unavailable aspects (not currently unlocked) can still be walked through,
but at a steep cost, so the search only uses them when there is no
similarly-short path through aspects you actually have.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .aspects import ADJACENCY, ASPECT_TABLE

UNAVAILABLE_COST = 100
AVAILABLE_COST = 1

State = Tuple[str, int]  # (aspect, hops so far)


@dataclass
class ConnectionResult:
    success: bool
    path: List[str] = field(default_factory=list)
    cost: int = 0
    message: str = ""


def find_connection(
    start: str,
    end: str,
    unavailable: Set[str],
    min_steps: int = 1,
    max_steps: int = 40,
) -> ConnectionResult:
    if start not in ASPECT_TABLE or end not in ASPECT_TABLE:
        return ConnectionResult(False, message="Unknown aspect.")

    start_state: State = (start, 0)
    dist: Dict[State, int] = {start_state: 0}
    parent: Dict[State, Optional[State]] = {start_state: None}
    heap: List[Tuple[int, State]] = [(0, start_state)]
    goal: Optional[State] = None

    while heap:
        cost, (node, hops) = heapq.heappop(heap)
        if cost > dist.get((node, hops), float("inf")):
            continue
        if node == end and hops > min_steps:
            goal = (node, hops)
            break
        if hops >= max_steps:
            continue
        for neighbor in ADJACENCY[node]:
            weight = UNAVAILABLE_COST if neighbor in unavailable else AVAILABLE_COST
            nstate: State = (neighbor, hops + 1)
            ncost = cost + weight
            if ncost < dist.get(nstate, float("inf")):
                dist[nstate] = ncost
                parent[nstate] = (node, hops)
                heapq.heappush(heap, (ncost, nstate))

    if goal is None:
        return ConnectionResult(
            False, message=f"No connection found within {max_steps} steps.",
        )

    path: List[str] = []
    state: Optional[State] = goal
    while state is not None:
        path.append(state[0])
        state = parent[state]
    path.reverse()

    return ConnectionResult(True, path=path, cost=dist[goal])
