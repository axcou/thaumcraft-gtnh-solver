// Orchestrates the Research Table Solver page: fetches the shared aspect
// data, wires the size/clear/solve controls, and ties together the board
// (hexboard.js), the palette (aspect-palette.js), and grid import/export
// (grid-io.js).

const statusEl = document.getElementById("status");
const packsEl = document.getElementById("packs");
const sizeSelect = document.getElementById("size");

let aspectData = { aspects: {}, flavor: {}, packs: {}, default_packs: [], complexity: {} };
let packSelector = null;

sizeSelect.addEventListener("change", () => {
  buildBoard(parseInt(sizeSelect.value, 10) - 1);
});

document.getElementById("clearBoard").addEventListener("click", () => {
  for (const cell of cells.values()) {
    cell.aspect = null;
    cell.barred = false;
    cell.base = false;
    cell.solved = false;
  }
  draw();
  statusEl.textContent = "";
  statusEl.className = "";
});

document.getElementById("solveBtn").addEventListener("click", async () => {
  statusEl.className = "";
  statusEl.textContent = "Solving...";
  const payload = {
    radius,
    packs: packSelector.checkedPacks(),
    // Only send the truly-given aspects and barred cells -- not cells the
    // previous solve filled in, or a re-solve would treat that old fill-in
    // as newly-given and find nothing left to do.
    cells: Array.from(cells.entries())
      .filter(([, c]) => (c.aspect && c.base) || c.barred)
      .map(([k, c]) => {
        const [q, r] = k.split(",").map(Number);
        return { q, r, aspect: c.aspect, barred: c.barred };
      }),
  };
  try {
    const resp = await fetch("/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await resp.json();
    for (const [, cell] of cells) {
      if (!cell.base) {
        cell.aspect = null;
        cell.solved = false;
      }
    }
    if (data.success) {
      for (const entry of data.assignment) {
        const cell = cells.get(key(entry.q, entry.r));
        if (cell) {
          cell.aspect = entry.aspect;
          cell.solved = true;
        }
      }
      statusEl.className = "ok";
      statusEl.textContent =
        `Solved in ${(data.elapsed * 1000).toFixed(1)} ms ` +
        `(${data.attempts} attempt(s), ${data.used_cells} cell(s) used).`;
    } else {
      statusEl.className = "error";
      statusEl.textContent = data.message || "No solution found.";
    }
    draw();
  } catch (err) {
    statusEl.className = "error";
    statusEl.textContent = "Could not reach the server: " + err;
  }
});

async function init() {
  const resp = await fetch("/aspects");
  aspectData = await resp.json();
  packSelector = renderPackSelector(packsEl, aspectData, renderAspectPalette);
  renderAspectPalette();
  buildBoard(parseInt(sizeSelect.value, 10) - 1);
}

init();
