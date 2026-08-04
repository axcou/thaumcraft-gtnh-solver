from tcsolver.aspects import ADJACENCY, can_connect
from tcsolver.connections import find_connection


def _verify_path(path, min_steps):
    hops = len(path) - 1
    assert hops > min_steps
    for a, b in zip(path, path[1:]):
        assert can_connect(a, b), f"{a} and {b} are not connectable"


def test_direct_neighbors_still_get_a_longer_path():
    # aer is a direct component of lux, but the default min_steps=1 rules
    # out the trivial 1-hop link.
    result = find_connection("aer", "lux", unavailable=set())
    assert result.success, result.message
    _verify_path(result.path, min_steps=1)


def test_min_steps_is_respected():
    result = find_connection("aer", "lux", unavailable=set(), min_steps=3)
    assert result.success, result.message
    _verify_path(result.path, min_steps=3)


def test_prefers_available_aspects_over_unavailable_ones():
    # Force the search to route around "lux" by making it very costly;
    # the resulting path should avoid it if an alternative of the same
    # length exists.
    baseline = find_connection("aer", "ignis", unavailable=set(), min_steps=1)
    penalized = find_connection("aer", "ignis", unavailable={"lux"}, min_steps=1)
    assert baseline.success and penalized.success
    assert penalized.cost >= baseline.cost
    if "lux" in baseline.path:
        assert "lux" not in penalized.path or penalized.cost > baseline.cost


def test_unknown_aspect_fails_gracefully():
    result = find_connection("not_an_aspect", "aer", unavailable=set())
    assert not result.success
    assert result.message
