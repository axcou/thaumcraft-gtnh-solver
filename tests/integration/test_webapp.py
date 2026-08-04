"""Flask-layer tests using the test client (no live server, no browser) --
these exercise webapp.py's routing/JSON-handling directly, which the
existing solver/connection-finder unit tests never touch and the
Playwright e2e tests only cover incidentally through the UI."""

import pytest

from tcsolver import aspects
from tcsolver.webapp import NAV, app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


# --- pages ---------------------------------------------------------------


@pytest.mark.parametrize(
    "path,heading",
    [
        ("/", "Research Table Solver"),
        ("/connections", "Connection Helper"),
        ("/combinations", "Aspect Combination"),
        ("/sources", "Aspect Sources"),
        ("/item-lookup", "Item Aspect Lookup"),
        ("/metallurgy", "Metallurgic Perfection"),
    ],
)
def test_each_page_loads_and_shows_its_heading(client, path, heading):
    resp = client.get(path)
    assert resp.status_code == 200
    assert heading.encode() in resp.data


@pytest.mark.parametrize("page", NAV)
def test_each_page_marks_its_own_tab_active(client, page):
    resp = client.get(page["path"])
    body = resp.data.decode()
    active_tab = f'class="tab active" href="{page["path"]}"'
    assert active_tab in body
    # and no *other* tab is also marked active
    for other in NAV:
        if other["slug"] == page["slug"]:
            continue
        assert f'class="tab active" href="{other["path"]}"' not in body


def test_unknown_route_is_a_404(client):
    assert client.get("/not-a-real-page").status_code == 404


# --- /aspects --------------------------------------------------------------


def test_aspects_endpoint_shape(client):
    data = client.get("/aspects").get_json()
    assert set(data) == {
        "aspects", "flavor", "packs", "default_packs", "complexity", "sources", "metallurgy",
    }
    assert data["aspects"] == aspects.ASPECT_TABLE
    assert data["packs"] == aspects.PACKS
    assert data["default_packs"] == aspects.DEFAULT_PACKS
    assert set(data["complexity"]) == set(data["aspects"])
    # every aspect with sources must be a real one, and every entry must
    # carry the fields the Aspect Sources page's filters rely on
    assert set(data["sources"]) <= set(data["aspects"])
    for entries in data["sources"].values():
        for entry in entries:
            assert set(entry) == {"item", "impurity", "highlight"}
            assert entry["highlight"] in (None, "good", "hard")
    # every metallurgy requirement must reference a real aspect
    for recipe in data["metallurgy"]:
        assert set(recipe) == {"metal", "requires"}
        for req in recipe["requires"]:
            assert set(req) == {"aspect", "amount"}
            assert req["aspect"] in aspects.ALL_ASPECTS


# --- /solve ----------------------------------------------------------------


def test_solve_connects_two_reachable_base_aspects(client):
    resp = client.post(
        "/solve",
        json={
            "radius": 3,
            "packs": ["vanilla_tc"],
            "cells": [
                {"q": 3, "r": 0, "aspect": "terra"},
                {"q": -3, "r": 0, "aspect": "aer"},
            ],
        },
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["used_cells"] == len(data["assignment"])
    assert data["used_cells"] > 0


def test_solve_defaults_radius_and_packs_when_omitted(client):
    resp = client.post("/solve", json={"cells": []})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["message"]  # "Nothing to connect ..."


def test_solve_ignores_cells_outside_the_board(client):
    resp = client.post(
        "/solve",
        json={"radius": 1, "cells": [{"q": 100, "r": 100, "aspect": "terra"}]},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["used_cells"] == 0


def test_solve_ignores_an_unknown_aspect_name_instead_of_erroring(client):
    # Regression test: an unrecognized aspect string used to reach
    # ADJACENCY[aspect] inside the solver and raise an unhandled KeyError.
    resp = client.post(
        "/solve",
        json={
            "radius": 2,
            "cells": [
                {"q": 0, "r": 0, "aspect": "not_a_real_aspect"},
                {"q": 2, "r": -2, "aspect": "terra"},
            ],
        },
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    # only "terra" counted as a base aspect, so there's nothing to connect
    assert data["message"]
    assert data["used_cells"] == 0


def test_solve_barred_cell_is_never_part_of_the_assignment(client):
    resp = client.post(
        "/solve",
        json={
            "radius": 2,
            "cells": [
                {"q": 0, "r": 0, "aspect": "aer"},
                {"q": 2, "r": -2, "aspect": "lux"},
                {"q": 1, "r": -1, "barred": True},
            ],
        },
    )
    data = resp.get_json()
    assert data["success"] is True
    assigned_coords = {(c["q"], c["r"]) for c in data["assignment"]}
    assert (1, -1) not in assigned_coords


# --- /connect ----------------------------------------------------------------


def test_connect_returns_a_valid_path(client):
    resp = client.post("/connect", json={"from": "aer", "to": "lux", "min_steps": 1})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["path"][0] == "aer"
    assert data["path"][-1] == "lux"


def test_connect_defaults_min_steps_and_packs_when_omitted(client):
    resp = client.post("/connect", json={"from": "aer", "to": "ignis"})
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True


def test_connect_reports_failure_for_an_unknown_aspect(client):
    resp = client.post("/connect", json={"from": "not_a_real_aspect", "to": "aer"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is False
    assert data["message"]


# --- static asset caching ---------------------------------------------------


def test_icons_are_cached_aggressively(client):
    resp = client.get("/static/icons/ignis.svg")
    assert resp.status_code == 200
    cache_control = resp.headers["Cache-Control"]
    assert "no-cache" not in cache_control
    assert "max-age" in cache_control


def test_css_and_js_are_not_cached_aggressively(client):
    # These change while the app is being worked on -- unlike the icons,
    # they must always be revalidated so edits show up without a hard
    # refresh (see cache_icons_aggressively's docstring in webapp.py).
    for path in ("/static/style.css", "/static/solver.js"):
        resp = client.get(path)
        assert resp.status_code == 200
        assert "no-cache" in resp.headers["Cache-Control"]


def test_item_aspects_dataset_is_served_as_json(client):
    resp = client.get("/static/data/item_aspects.json")
    assert resp.status_code == 200
    data = resp.get_json()
    assert set(data) == {"aspects", "items"}
    assert len(data["items"]) > 10_000
