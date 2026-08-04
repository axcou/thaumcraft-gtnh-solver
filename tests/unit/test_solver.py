import time

from tcsolver import aspects
from tcsolver.hexboard import HexBoard
from tcsolver.solver import solve, verify_solution


def make_board(radius, base, barred=()):
    board = HexBoard(radius)
    for coord, aspect in base.items():
        cell = board.cells[coord]
        cell.aspect = aspect
        cell.base = True
    for coord in barred:
        board.cells[coord].barred = True
    return board


VANILLA = aspects.enabled_aspects(["vanilla_tc"])
GTNH = aspects.enabled_aspects(
    ["vanilla_tc", "forbidden_magic", "gregtech", "magic_bees", "avaritia"]
)


def test_prefers_simple_aspects_over_fewer_cells():
    # telum's only aspect-graph neighbors are ignis (complexity 0),
    # instrumentum (complexity 6) and ira (complexity 8); ira is the *only*
    # single-tile connector between telum and ignis, but it's a very
    # complex aspect. The solver should prefer spending an extra tile on
    # simple aspects (ignis, then something built from it) over the
    # one-tile-but-complex "ira" shortcut.
    board = make_board(radius=3, base={(2, 0): "telum", (0, 0): "ignis"})
    result = solve(board, VANILLA)
    assert result.success, result.message
    assert verify_solution(board, result.assignment)
    assert "ira" not in result.assignment.values()
    assert result.used_cells > 1, "expected the solver to spend an extra tile to avoid ira"
    total_complexity = sum(aspects.COMPLEXITY[a] for a in result.assignment.values())
    assert total_complexity < aspects.COMPLEXITY["ira"]


def test_three_corners_no_obstacles():
    board = make_board(
        radius=2,
        base={(2, -2): "terra", (-2, 2): "aqua", (0, -2): "ignis"},
    )
    result = solve(board, VANILLA)
    assert result.success, result.message
    assert verify_solution(board, result.assignment)


def test_two_aspects_forced_detour_around_barred_ring():
    ring = [(1, 0), (0, -1), (-1, 0), (-1, 1), (0, 1)]  # all distance-1 neighbors except (1,-1)
    board = make_board(
        radius=2,
        base={(0, 0): "aer", (2, -2): "lux"},
        barred=ring,
    )
    result = solve(board, VANILLA)
    assert result.success, result.message
    assert verify_solution(board, result.assignment)
    for coord in ring:
        assert coord not in result.assignment


def test_larger_hexagon_many_base_aspects():
    board = make_board(
        radius=4,
        base={
            (4, 0): "terra",
            (0, 4): "instrumentum",
            (-4, 0): "aer",
            (0, -4): "praecantatio",
            (4, -4): "ordo",
            (-4, 4): "arbor",
        },
        barred={(1, 0), (2, -2), (-2, 1), (0, 2), (3, -1), (-1, -2)},
    )
    result = solve(board, GTNH)
    assert result.success, result.message
    assert verify_solution(board, result.assignment)


def test_impossible_board_fails_gracefully():
    # terra and aer are both primal (unrelated) aspects: they cannot connect
    # directly, and every other cell is barred, so there is no room for a
    # linking chain. The solver must fail fast with a clear message rather
    # than hang or raise.
    board = HexBoard(1)
    board.cells[(0, 0)].aspect = "terra"
    board.cells[(0, 0)].base = True
    board.cells[(1, 0)].aspect = "aer"
    board.cells[(1, 0)].base = True
    for coord, cell in board.cells.items():
        if coord not in ((0, 0), (1, 0)):
            cell.barred = True
    start = time.perf_counter()
    result = solve(board, set(), time_budget=1.0)
    elapsed = time.perf_counter() - start
    assert not result.success
    assert result.message
    assert elapsed < 1.0


def test_solve_speed_on_big_board():
    board = make_board(
        radius=5,
        base={
            (5, 0): "terra",
            (0, 5): "instrumentum",
            (-5, 0): "aer",
            (0, -5): "praecantatio",
            (5, -5): "ordo",
            (-5, 5): "arbor",
            (3, 2): "ignis",
            (-3, -2): "victus",
        },
        barred={(1, 1), (-1, -1), (2, 0), (-2, 0), (0, 2), (0, -2)},
    )
    start = time.perf_counter()
    result = solve(board, GTNH)
    elapsed = time.perf_counter() - start
    assert result.success, result.message
    assert verify_solution(board, result.assignment)
    assert elapsed < 1.0, f"solve took {elapsed:.3f}s, expected < 1.0s"
