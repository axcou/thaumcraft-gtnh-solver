"""Geometry invariants for the axial-coordinate hex board -- these are
cheap to check exhaustively and catch a broken direction table or
distance formula long before it surfaces as a weird solver result."""

from collections import deque

import pytest

from tcsolver.hexboard import HexBoard


def test_radius_zero_is_a_single_cell():
    board = HexBoard(0)
    assert len(board) == 1
    assert (0, 0) in board


def test_negative_radius_is_rejected():
    with pytest.raises(ValueError):
        HexBoard(-1)


@pytest.mark.parametrize("radius", [1, 2, 3, 4, 5])
def test_cell_count_matches_the_hexagonal_number_formula(radius):
    board = HexBoard(radius)
    assert len(board) == 3 * radius**2 + 3 * radius + 1


@pytest.mark.parametrize("radius", [1, 2, 3])
def test_neighbors_are_mutual(radius):
    board = HexBoard(radius)
    for coord in board.cells:
        for neighbor in board.neighbors(coord):
            assert coord in board.neighbors(neighbor), f"{coord} -> {neighbor} is one-directional"


def test_neighbors_are_within_the_board_and_distinct():
    board = HexBoard(2)
    for coord in board.cells:
        neighbors = board.neighbors(coord)
        assert len(neighbors) == len(set(neighbors))
        for n in neighbors:
            assert n in board
            assert n != coord


def _bfs_distance(board, start, goal):
    if start == goal:
        return 0
    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        coord, dist = queue.popleft()
        for neighbor in board.neighbors(coord):
            if neighbor == goal:
                return dist + 1
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, dist + 1))
    raise AssertionError(f"no path from {start} to {goal}")


def test_distance_matches_actual_shortest_path_length():
    # Cross-check the closed-form hex distance formula against a real BFS
    # over the neighbor graph, for a spread of same-board coordinate pairs.
    board = HexBoard(4)
    pairs = [
        ((0, 0), (4, 0)),
        ((0, 0), (0, -4)),
        ((4, 0), (-4, 4)),
        ((2, -3), (-1, 2)),
        ((0, 0), (0, 0)),
    ]
    for a, b in pairs:
        assert HexBoard.distance(a, b) == _bfs_distance(board, a, b), f"{a} <-> {b}"


def test_coordinates_outside_the_radius_are_excluded():
    board = HexBoard(2)
    assert (2, 0) in board
    assert (3, 0) not in board
    assert (0, 3) not in board
    assert (-3, 3) not in board


def test_reset_clears_every_cell():
    board = HexBoard(1)
    for cell in board:
        cell.aspect = "terra"
        cell.barred = True
        cell.base = True
    board.reset()
    for cell in board:
        assert cell.aspect is None
        assert cell.barred is False
        assert cell.base is False
