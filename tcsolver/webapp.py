"""Local web app: hex board editor + fast solver, served over Flask."""

from __future__ import annotations

import os
from typing import Any

from flask import Flask, jsonify, render_template, request

from . import aspects
from .connections import find_connection
from .hexboard import HexBoard
from .solver import solve
from .sources import ASPECT_SOURCES

app = Flask(__name__)


def static_version(filename: str) -> int:
    """Last-modified time of a static file, used as a cache-busting query
    string (see templates/base.html) -- whenever a CSS/JS file is edited,
    its URL changes automatically, so browsers can never serve a stale
    cached copy of it after a change, no manual hard-refresh needed."""
    path = os.path.join(app.static_folder, filename)
    try:
        return int(os.path.getmtime(path))
    except OSError:
        return 0


app.jinja_env.globals["static_version"] = static_version


@app.after_request
def cache_icons_aggressively(response: Any) -> Any:
    # The ~70 aspect icons never change, so browsers can cache them for a
    # long time -- that's most of what made the palette take 1-2s to paint
    # in on every visit. CSS/JS/HTML are deliberately left on Flask's
    # default (always-revalidated) behavior, since those *do* change while
    # this app is being worked on; a blanket long cache on them would hide
    # edits behind a stale browser cache instead.
    if request.path.startswith("/static/icons/"):
        # Werkzeug's static handler sets "no-cache" by default (always
        # revalidate) -- clear it, or it overrides max-age and forces a
        # round-trip on every request regardless.
        response.cache_control.no_cache = None
        response.cache_control.public = True
        response.cache_control.max_age = 60 * 60 * 24 * 7
    return response

# The site's tab bar: one entry per page, in display order.
NAV = [
    {"slug": "solver", "path": "/", "label": "Research Table Solver"},
    {"slug": "connections", "path": "/connections", "label": "Connection Helper"},
    {"slug": "combinations", "path": "/combinations", "label": "Aspect Combination"},
    {"slug": "sources", "path": "/sources", "label": "Aspect Sources"},
]


@app.get("/")
def solver_page() -> Any:
    return render_template("solver.html", active="solver", nav=NAV)


@app.get("/connections")
def connections_page() -> Any:
    return render_template("connections.html", active="connections", nav=NAV)


@app.get("/combinations")
def combinations_page() -> Any:
    return render_template("combinations.html", active="combinations", nav=NAV)


@app.get("/sources")
def sources_page() -> Any:
    return render_template("sources.html", active="sources", nav=NAV)


@app.get("/aspects")
def get_aspects() -> Any:
    return jsonify(
        {
            "aspects": aspects.ASPECT_TABLE,
            "flavor": aspects.FLAVOR,
            "packs": aspects.PACKS,
            "default_packs": aspects.DEFAULT_PACKS,
            "complexity": aspects.COMPLEXITY,
            "sources": ASPECT_SOURCES,
        }
    )


@app.post("/solve")
def post_solve() -> Any:
    payload = request.get_json(force=True)
    radius = int(payload.get("radius", 4))
    packs = payload.get("packs", aspects.DEFAULT_PACKS)
    cells = payload.get("cells", [])

    board = HexBoard(radius)
    for entry in cells:
        coord = (int(entry["q"]), int(entry["r"]))
        if coord not in board:
            continue
        cell = board.cells[coord]
        aspect = entry.get("aspect")
        if aspect and aspect in aspects.ALL_ASPECTS:
            cell.aspect = aspect
            cell.base = True
        cell.barred = bool(entry.get("barred", False))

    enabled = aspects.enabled_aspects(packs)
    # Base aspects are always usable, even if their pack was unchecked after
    # the fact -- they're already placed on the board.
    enabled |= {cell.aspect for cell in board if cell.base and cell.aspect}

    result = solve(board, enabled)

    return jsonify(
        {
            "success": result.success,
            "assignment": [
                {"q": q, "r": r, "aspect": aspect}
                for (q, r), aspect in result.assignment.items()
            ],
            "used_cells": result.used_cells,
            "elapsed": result.elapsed,
            "attempts": result.attempts,
            "message": result.message,
        }
    )


@app.post("/connect")
def post_connect() -> Any:
    payload = request.get_json(force=True)
    start = payload.get("from")
    end = payload.get("to")
    min_steps = int(payload.get("min_steps", 1))
    packs = payload.get("packs", aspects.DEFAULT_PACKS)

    available = aspects.enabled_aspects(packs)
    unavailable = aspects.ALL_ASPECTS - available

    result = find_connection(start, end, unavailable, min_steps=min_steps)

    return jsonify(
        {
            "success": result.success,
            "path": result.path,
            "cost": result.cost,
            "message": result.message,
        }
    )


def main() -> None:
    # threaded=True lets the dev server handle the ~70 concurrent icon
    # requests in parallel instead of one at a time, which is what made
    # the aspect palette take 1-2s to paint in.
    app.run(host="127.0.0.1", port=5000, debug=True, threaded=True)


if __name__ == "__main__":
    main()
