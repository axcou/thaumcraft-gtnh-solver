# Thaumcraft Research Solver (GTNH)

A fast Python reimplementation of the Thaumcraft research-table hex board
solver (the mini-game where you have to link aspects on a hexagonal grid),
inspired by:

- [ythri/tcresearch](https://github.com/ythri/tcresearch/tree/gh-pages)
- [SkilledAlpaca/universal_tc_research_solver](https://github.com/SkilledAlpaca/universal_tc_research_solver/)

## Why a reimplementation

The reference JS solver (`universal_tc_research_solver`) `deepcopy()`s the
**entire grid at every single step** of its backtracking, and explores the
board cell by cell with a naive DFS -- this can get very slow (or even get
stuck) on a moderately busy board.

This version replaces that with:
- a **BFS** over `(cell, aspect)` states to connect two components -- since
  every extra cell costs exactly 1, the first path BFS finds is already the
  shortest one, no cell-by-cell trial and error needed;
- a Steiner-tree heuristic (always connect the closest pair of components
  first) to decide the order in which components get merged;
- backtracking that only re-copies small dictionaries (components, used
  cells), never the whole grid.

Result: the heaviest test board (radius 5, 8 base aspects, every GTNH pack
enabled) solves in a few milliseconds (see
`tests/test_solver.py::test_solve_speed_on_big_board`).

## Structure

```
thaumcraft_gtnh/
├── requirements.txt
├── README.md
├── tcsolver/
│   ├── aspects.py            # aspect combination table (Vanilla + GTNH) + packs
│   ├── hexboard.py           # hexagonal geometry (axial coordinates)
│   ├── solver.py             # research-table board solving algorithm
│   ├── connections.py        # aspect-to-aspect connection finder
│   ├── sources.py            # curated cheap/pure item sources per aspect
│   ├── metallurgy.py         # Metallurgic Perfection infusion recipes per metal
│   ├── webapp.py             # Flask server: page routes, /aspects, /solve, /connect
│   ├── templates/
│   │   ├── base.html             # shared shell: tab nav + content block
│   │   ├── solver.html           # Research Table Solver
│   │   ├── connections.html      # Connection Helper
│   │   ├── combinations.html     # Aspect Combination
│   │   ├── sources.html          # Aspect Sources
│   │   └── metallurgy.html       # Metallurgic Perfection
│   └── static/
│       ├── style.css
│       ├── utils.js              # shared: capitalize(), icon-tile helper
│       ├── packs.js              # shared: "Active mods" widget + GTNH preset
│       ├── hexboard.js           # Solver: geometry, board state, canvas render
│       ├── aspect-palette.js     # Solver: draggable aspect palette
│       ├── grid-io.js            # Solver: click/drop, .tcgrid + PNG import/export
│       ├── solver.js             # Solver: page wiring (size/clear/solve) + init
│       ├── connections.js        # Connection Helper: page logic
│       ├── aspect-tree.js        # Aspect Combination: pan/zoom + tree diagram
│       ├── combinations.js       # Aspect Combination: aspect list/search + init
│       ├── aspect-sources.js     # Aspect Sources: card grid + filters + init
│       ├── metallurgy.js         # Metallurgic Perfection: recipe table + search
│       └── icons/                # 72 aspect SVGs (game-icons.net, CC BY 3.0)
└── tests/
    ├── unit/               # pure Python, no Flask/network -- fast, run these most
    │   ├── test_aspects.py       # ASPECT_TABLE/PACKS/complexity invariants
    │   ├── test_hexboard.py      # hex geometry (neighbors, distance, cell count)
    │   ├── test_solver.py        # board-solving algorithm
    │   ├── test_connections.py   # aspect-to-aspect connection finder
    │   ├── test_sources.py       # ASPECT_SOURCES invariants
    │   └── test_metallurgy.py    # METALLURGIC_RECIPES invariants
    ├── integration/
    │   └── test_webapp.py        # Flask routes/JSON via test_client, no live server
    └── e2e/
        ├── conftest.py            # live Flask server + Playwright fixtures
        └── test_browser.py        # tree rendering/pan-zoom, canvas interaction,
                                    # grid import/export, connection helper
```

## Installation

```
pip install -r requirements.txt
```

## Running the tests

```
pytest tests/                  # everything
pytest tests/unit              # fast, no Flask/browser -- the ones to run while iterating
pytest tests/integration        # Flask routes/JSON, via the test client (still no browser)
pytest tests/e2e                # full browser end-to-end
```

`tests/e2e` drives the app through an actual browser (via Playwright) to
check things the other two layers can't: the Aspect Combination tree's DOM
structure and connector lines, wheel-zoom/drag-pan, canvas clicks and grid
import/export on the Solver page, the GTNH pack preset, and the Connection
Helper's result chain. It launches your system's installed Edge (falling
back to Chrome, then Playwright's own Chromium) headlessly against a real
instance of the Flask app on a throwaway port -- no `playwright install`
needed as long as Edge or Chrome is present. If neither is found, those
tests skip themselves instead of failing.

## Running the web app

```
python -m tcsolver.webapp
```

Then open <http://localhost:5000>. The site has 5 tabs:

- **Research Table Solver** -- the hex board solver.
  - Pick a board size (3 to 6 -- the board regenerates automatically) and
    which mods are active (the GTNH preset -- Vanilla TC, Forbidden Magic,
    Gregtech, Magic Bees -- is on by default; Avaritia and a few other
    GT:NH packs are also available).
  - Drag an aspect from a side panel onto a cell to place an aspect already
    revealed by the research in progress.
  - Click a cell to clear it (aspect or bar); on an empty cell, that bars/
    unbars it instead -- no separate mode needed.
  - Click "Solve": the cells to fill in (and which aspect to place there)
    are highlighted with a gold outline.
  - "Export grid" / "Import grid" save and reload a board (size, active
    mods, base/barred/solved cells) as a `.tcgrid` file -- a plain JSON
    document under a distinct extension, so the file picker only ever
    offers grid files. "Export image" instead saves a cropped PNG
    snapshot of the board as currently drawn.
- **Connection Helper** -- pick a "from" and "to" aspect and a minimum
  number of steps, and it finds the cheapest walk between them in the
  combination graph (preferring aspects from your active mods).
- **Aspect Combination** -- a searchable reference of every aspect and
  what it is made from (or "Primal aspect" if it has no components).
- **Aspect Sources** -- a searchable, filterable reference of cheap item
  sources for each aspect (community-curated), one card per aspect. Each
  entry shows its impurity count; "Pure sources only" keeps just the
  0-impurity ones, "Especially good only" keeps the sheet's green
  (especially good/surprising) picks -- red-flagged entries (pure, but
  hard to get) are shown in both.
- **Metallurgic Perfection** -- a searchable table of every metal and how
  many of which aspects its nugget needs to be infused with, restricted
  to your active mods (a metal disappears if any of its required aspects
  belongs to a disabled pack).

## Icons

The aspect icons (`tcsolver/static/icons/*.svg`) come from
[game-icons.net](https://game-icons.net/) (authors Lorc, Delapouite,
Cathelineau -- [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)),
via `universal_tc_research_solver`'s source list (`icon_sources.txt`).

## Reference data from the community spreadsheet

`tcsolver/sources.py` and `tcsolver/metallurgy.py` are straight ports of
two tabs of the community-maintained
["EasyPure Aspect Sources" spreadsheet](https://docs.google.com/spreadsheets/d/1Llvu91Vmn4RcCE__lKV8p_MIR9tiaV2URGbkombvlkE):
"EasyPure Aspect Sources" itself (including its green/especially-good and
red/pure-but-hard highlighting -- neither covers every aspect, only the
ones each sheet tab lists) and "Metallurgic Perfection Recipes".

## Using it as a library

```python
from tcsolver import aspects
from tcsolver.hexboard import HexBoard
from tcsolver.solver import solve

board = HexBoard(radius=4)
board.cells[(4, 0)].aspect = "terra"
board.cells[(4, 0)].base = True
board.cells[(-4, 0)].aspect = "aer"
board.cells[(-4, 0)].base = True

enabled = aspects.enabled_aspects(["vanilla_tc", "gregtech"])
result = solve(board, enabled)
print(result.assignment, result.used_cells, result.elapsed)
```
