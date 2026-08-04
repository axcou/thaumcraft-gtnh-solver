"""Hexagon-shaped board of hexagonal cells, in axial coordinates.

The original tools (ythri/tcresearch, SkilledAlpaca/universal_tc_research_solver)
lay their board out as a hexagon of `grid_size` cells per side, using
column-offset array indices with three different neighbor rules depending on
which half of the board a column falls in. That is equivalent to a standard
hexagon of radius R = grid_size - 1 in axial coordinates (q, r), which has a
single, uniform neighbor rule -- much simpler to reason about and to test.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, List, Tuple

Coord = Tuple[int, int]

# The 6 axial hex directions.
AXIAL_DIRECTIONS: Tuple[Coord, ...] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)


@dataclass
class Cell:
    coord: Coord
    aspect: str | None = None
    barred: bool = False
    base: bool = False  # True if this cell's aspect was given (not solved for)


class HexBoard:
    """Hexagon-shaped board of radius `radius` (radius 0 == a single cell)."""

    def __init__(self, radius: int):
        if radius < 0:
            raise ValueError("radius must be >= 0")
        self.radius = radius
        self.cells: Dict[Coord, Cell] = {}
        for q in range(-radius, radius + 1):
            r_lo = max(-radius, -q - radius)
            r_hi = min(radius, -q + radius)
            for r in range(r_lo, r_hi + 1):
                self.cells[(q, r)] = Cell((q, r))

    def __contains__(self, coord: Coord) -> bool:
        return coord in self.cells

    def __iter__(self) -> Iterator[Cell]:
        return iter(self.cells.values())

    def __len__(self) -> int:
        return len(self.cells)

    def neighbors(self, coord: Coord) -> List[Coord]:
        q, r = coord
        result = []
        for dq, dr in AXIAL_DIRECTIONS:
            n = (q + dq, r + dr)
            if n in self.cells:
                result.append(n)
        return result

    @staticmethod
    def distance(a: Coord, b: Coord) -> int:
        aq, ar = a
        bq, br = b
        return (abs(aq - bq) + abs(ar - br) + abs((aq + ar) - (bq + br))) // 2

    def reset(self) -> None:
        for cell in self.cells.values():
            cell.aspect = None
            cell.barred = False
            cell.base = False
