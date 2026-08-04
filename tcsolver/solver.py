"""Fast solver for the Thaumcraft hex research board.

Given a HexBoard with some "base" cells already carrying a fixed aspect and
some cells barred (unusable), find aspects for a subset of the remaining
free cells so that every base cell ends up in a single connected component,
where two grid-adjacent cells are considered connected iff their aspects
satisfy `can_connect` (one is a direct recipe component of the other).

This targets the same problem as SkilledAlpaca/universal_tc_research_solver's
`main_loop()`/`find_path()`, but replaces its per-cell backtracking (which
deep-copies the *entire* grid on every single step) with:

  * A Dijkstra search over (cell, aspect) states to connect two components,
    weighted primarily by how simple (low crafting-step) the aspects placed
    along the way are, and only secondarily by how many tiles that takes --
    so the search happily spends an extra tile or two if it means using
    aspects the player is more likely to already have on hand, rather than
    always chasing the absolute minimum tile count.
  * A classic nearest-component-first Steiner-tree heuristic to decide which
    two components to connect next.
  * Backtracking, when a merge turns out to be a dead end, over cheap
    O(#components) snapshots instead of over the whole board.
"""

from __future__ import annotations

import heapq
import itertools
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .aspects import ADJACENCY, COMPLEXITY, can_connect
from .hexboard import Coord, HexBoard

Component = Dict[Coord, str]


@dataclass
class SolveResult:
    success: bool
    assignment: Dict[Coord, str] = field(default_factory=dict)
    used_cells: int = 0
    elapsed: float = 0.0
    attempts: int = 0
    message: str = ""


def _bfs_connect(
    board: HexBoard,
    free_cells: Set[Coord],
    source: Component,
    target: Component,
    enabled: Set[str],
) -> Optional[List[Tuple[Coord, str]]]:
    """Cheapest chain of new (cell, aspect) tiles connecting `source` to `target`.

    "Cheapest" is primarily about simplicity: the total crafting-step
    complexity of the aspects placed along the way is minimized first, and
    the number of tiles used is only a tie-breaker after that -- so a longer
    chain through primal/simple aspects is preferred over a shorter one that
    needs a deeply-crafted aspect.

    `source`/`target` map every cell currently in each component to its
    (already fixed) aspect -- the search may enter or leave a component
    through any of its cells, not just a single designated frontier cell.

    Returns the new intermediate (cell, aspect) pairs to add (excludes the
    source/target cells themselves), or None if unreachable.
    """
    State = Tuple[Coord, str]
    # A single virtual sink representing "reached the target component" --
    # letting it flow through the normal Dijkstra pop/settle order (instead
    # of tracking "the best goal so far" by hand) is what makes the search
    # correct when several target cells could be reached at different costs.
    GOAL = object()

    # priority = (total complexity of new tiles so far, number of hops so far)
    best: Dict[object, Tuple[int, int]] = {}
    parent: Dict[object, Optional[State]] = {}
    counter = itertools.count()  # tie-break so the heap never compares states
    heap: List[Tuple[Tuple[int, int], int, object]] = []

    for cell, aspect in source.items():
        state = (cell, aspect)
        if state not in best:
            best[state] = (0, 0)
            parent[state] = None
            heapq.heappush(heap, ((0, 0), next(counter), state))

    reached_goal = False
    while heap:
        priority, _, state = heapq.heappop(heap)
        if priority > best[state]:
            continue  # stale entry, a cheaper route to this state already won
        if state is GOAL:
            reached_goal = True
            break
        cell, aspect = state
        complexity_so_far, hops = priority

        for ncell in board.neighbors(cell):
            if ncell in target:
                naspect = target[ncell]
                if not can_connect(aspect, naspect):
                    continue
                # Reaching the target doesn't add a new tile, so its cost is
                # the same as the state we're leaving -- but hops still grows,
                # to prefer fewer tiles among equally-simple connections.
                npriority = (complexity_so_far, hops + 1)
                if GOAL not in best or npriority < best[GOAL]:
                    best[GOAL] = npriority
                    parent[GOAL] = state
                    heapq.heappush(heap, (npriority, next(counter), GOAL))
                continue
            if ncell not in free_cells:
                continue
            for naspect in ADJACENCY[aspect]:
                if naspect not in enabled:
                    continue
                nstate = (ncell, naspect)
                npriority = (complexity_so_far + COMPLEXITY[naspect], hops + 1)
                if nstate in best and best[nstate] <= npriority:
                    continue
                best[nstate] = npriority
                parent[nstate] = state
                heapq.heappush(heap, (npriority, next(counter), nstate))

    if not reached_goal:
        return None

    path: List[State] = []
    state: Optional[State] = parent[GOAL]
    while state is not None:
        path.append(state)
        state = parent[state]
    path.reverse()
    # path[0] is a source state; the target itself was never added to path.
    return path[1:]


def _component_pairs_by_distance(
    board: HexBoard, components: List[Component]
) -> List[Tuple[int, int, int]]:
    pairs = []
    for i in range(len(components)):
        for j in range(i + 1, len(components)):
            d = min(
                board.distance(a, b) for a in components[i] for b in components[j]
            )
            pairs.append((d, i, j))
    pairs.sort(key=lambda t: t[0])
    return pairs


def _solve_rec(
    board: HexBoard,
    components: List[Component],
    used: Set[Coord],
    assignment: Dict[Coord, str],
    barred: Set[Coord],
    all_cells: Set[Coord],
    enabled: Set[str],
    deadline: float,
    counter: List[int],
    max_attempts: int,
) -> Optional[Dict[Coord, str]]:
    if len(components) <= 1:
        return assignment
    if time.perf_counter() > deadline or counter[0] >= max_attempts:
        return None

    for _dist, i, j in _component_pairs_by_distance(board, components):
        counter[0] += 1
        if counter[0] >= max_attempts or time.perf_counter() > deadline:
            return None

        free = all_cells - used - barred
        chain = _bfs_connect(board, free, components[i], components[j], enabled)
        if chain is None:
            continue

        new_assignment = dict(assignment)
        new_used = set(used)
        for cell, aspect in chain:
            new_assignment[cell] = aspect
            new_used.add(cell)

        merged: Component = {**components[i], **components[j], **dict(chain)}
        remaining = [c for k, c in enumerate(components) if k not in (i, j)]
        remaining.append(merged)

        result = _solve_rec(
            board, remaining, new_used, new_assignment, barred, all_cells,
            enabled, deadline, counter, max_attempts,
        )
        if result is not None:
            return result
        # else: this merge was a dead end for the rest of the board -- try
        # the next-closest pair instead (cheap: no board state was mutated).

    return None


def solve(
    board: HexBoard,
    enabled: Set[str],
    time_budget: float = 5.0,
    max_attempts: int = 20000,
) -> SolveResult:
    """Solve `board` in place-compatible fashion: returns new aspect placements."""
    start = time.perf_counter()

    base_cells: Component = {
        coord: cell.aspect
        for coord, cell in board.cells.items()
        if cell.base and cell.aspect
    }
    barred = {coord for coord, cell in board.cells.items() if cell.barred}
    all_cells = set(board.cells)

    if len(base_cells) <= 1:
        return SolveResult(
            success=True, assignment={}, used_cells=0,
            elapsed=time.perf_counter() - start,
            message="Nothing to connect (0 or 1 base aspect).",
        )

    components: List[Component] = [{coord: aspect} for coord, aspect in base_cells.items()]
    used = set(base_cells)
    counter = [0]
    deadline = start + time_budget

    result = _solve_rec(
        board, components, used, {}, barred, all_cells, enabled, deadline,
        counter, max_attempts,
    )

    elapsed = time.perf_counter() - start
    if result is None:
        return SolveResult(
            success=False, assignment={}, used_cells=0, elapsed=elapsed,
            attempts=counter[0],
            message="No connecting layout found within the search budget.",
        )
    return SolveResult(
        success=True, assignment=result, used_cells=len(result),
        elapsed=elapsed, attempts=counter[0],
    )


def verify_solution(board: HexBoard, assignment: Dict[Coord, str]) -> bool:
    """Re-check (independently of the solver) that `assignment` connects all
    base cells of `board` into one component, using no barred cells."""
    barred = {coord for coord, cell in board.cells.items() if cell.barred}
    aspect_of: Dict[Coord, str] = {
        coord: cell.aspect for coord, cell in board.cells.items()
        if cell.base and cell.aspect
    }
    for coord, aspect in assignment.items():
        if coord in barred or coord in aspect_of:
            return False
        aspect_of[coord] = aspect

    base_cells = [coord for coord, cell in board.cells.items() if cell.base and cell.aspect]
    if len(base_cells) <= 1:
        return True

    start = base_cells[0]
    seen = {start}
    dq = deque([start])
    while dq:
        cell = dq.popleft()
        for ncell in board.neighbors(cell):
            if ncell in seen or ncell not in aspect_of:
                continue
            if can_connect(aspect_of[cell], aspect_of[ncell]):
                seen.add(ncell)
                dq.append(ncell)

    return all(coord in seen for coord in base_cells)
