// Canvas interactions (click to bar/clear, drop to place an aspect) and
// grid/image import & export for the Research Table Solver. Depends on
// hexboard.js (canvas, cells, key, etc.) and reaches into solver.js's
// `radius`/`packSelector`/`statusEl`/`sizeSelect` from its callbacks.

// Click: erase whatever is on the cell (aspect or barred); on an empty
// cell, toggle barred instead. No separate "mode" needed.
canvas.addEventListener("click", (evt) => {
  const [px, py] = eventToCanvasPixel(evt);
  const k = cellAtPixel(px, py);
  if (!k) return;
  const cell = cells.get(k);
  if (cell.aspect) {
    cell.aspect = null;
    cell.base = false;
    cell.solved = false;
  } else if (cell.barred) {
    cell.barred = false;
  } else {
    cell.barred = true;
  }
  draw();
});

canvas.addEventListener("dragover", (evt) => {
  evt.preventDefault();
});

canvas.addEventListener("drop", (evt) => {
  evt.preventDefault();
  const aspect = evt.dataTransfer.getData("text/plain");
  if (!aspect) return;
  const [px, py] = eventToCanvasPixel(evt);
  const k = cellAtPixel(px, py);
  if (!k) return;
  const cell = cells.get(k);
  cell.aspect = aspect;
  cell.base = true;
  cell.barred = false;
  cell.solved = false;
  draw();
});

// The canvas itself is always sized for the biggest possible board so its
// background never resizes (see resizeCanvas); exporting the raw canvas
// would mean mostly empty margin for anything smaller than size 6, so crop
// to just the current board's cells (plus a small margin) instead.
function boardBoundingBox() {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const [k] of cells) {
    const [q, r] = k.split(",").map(Number);
    const [cx, cy] = axialToPixel(q, r);
    minX = Math.min(minX, cx - HEX_SIZE);
    maxX = Math.max(maxX, cx + HEX_SIZE);
    minY = Math.min(minY, cy - HEX_SIZE);
    maxY = Math.max(maxY, cy + HEX_SIZE);
  }
  const margin = 16;
  const x = Math.max(0, minX - margin);
  const y = Math.max(0, minY - margin);
  const width = Math.min(canvas.width - x, maxX - minX + margin * 2);
  const height = Math.min(canvas.height - y, maxY - minY + margin * 2);
  return { x, y, width, height };
}

document.getElementById("exportBtn").addEventListener("click", () => {
  const box = boardBoundingBox();
  const exportCanvas = document.createElement("canvas");
  exportCanvas.width = box.width;
  exportCanvas.height = box.height;
  exportCanvas
    .getContext("2d")
    .drawImage(canvas, box.x, box.y, box.width, box.height, 0, 0, box.width, box.height);

  const link = document.createElement("a");
  link.download = `thaumcraft-research-size${radius + 1}.png`;
  link.href = exportCanvas.toDataURL("image/png");
  link.click();
});

// Custom extension for saved grids: still plain JSON underneath, but a
// distinct extension means the file picker (accept=".tcgrid" on the
// import <input>) only ever offers grid files, not just any .json lying
// around, and double-clicking one in a file browser is unambiguously
// "open with this app" rather than "a generic JSON file".
const GRID_FILE_EXTENSION = ".tcgrid";

// Generic, memorable two-word names for exported grids (e.g. "silent-comet"),
// instead of a filename tied to the board size -- easier to tell apart in a
// downloads folder full of them.
const NAME_ADJECTIVES = [
  "brave", "calm", "clever", "eager", "fuzzy", "gentle", "happy", "icy",
  "jolly", "keen", "lively", "mighty", "noble", "proud", "quiet", "rapid",
  "silent", "tidy", "upbeat", "vivid", "witty", "zesty", "bold", "crisp",
  "daring", "earnest", "fancy", "glad", "humble", "jovial",
];
const NAME_NOUNS = [
  "falcon", "otter", "maple", "comet", "harbor", "lantern", "meadow",
  "pebble", "river", "summit", "tiger", "willow", "canyon", "ember",
  "glacier", "horizon", "island", "juniper", "kestrel", "lagoon", "mirage",
  "nebula", "oasis", "panther", "quartz", "reef", "sparrow", "thicket",
  "valley", "whisper",
];

function randomGridName() {
  const adjective = NAME_ADJECTIVES[Math.floor(Math.random() * NAME_ADJECTIVES.length)];
  const noun = NAME_NOUNS[Math.floor(Math.random() * NAME_NOUNS.length)];
  return `${adjective}-${noun}`;
}

function exportGridState() {
  return {
    version: 1,
    radius,
    packs: packSelector.checkedPacks(),
    cells: Array.from(cells.entries())
      .filter(([, c]) => c.aspect || c.barred)
      .map(([k, c]) => {
        const [q, r] = k.split(",").map(Number);
        return { q, r, aspect: c.aspect, base: c.base, solved: c.solved, barred: c.barred };
      }),
  };
}

function importGridState(data) {
  const newRadius = Number.isInteger(data.radius) ? data.radius : radius;
  const size = Math.min(6, Math.max(3, newRadius + 1));
  sizeSelect.value = String(size);
  buildBoard(size - 1);

  if (Array.isArray(data.packs)) {
    packSelector.setPacks(data.packs);
  }
  renderAspectPalette();

  for (const entry of data.cells || []) {
    const cell = cells.get(key(entry.q, entry.r));
    if (!cell) continue;
    cell.aspect = entry.aspect || null;
    cell.base = Boolean(entry.base);
    cell.solved = Boolean(entry.solved);
    cell.barred = Boolean(entry.barred);
  }
  draw();
}

document.getElementById("exportGridBtn").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(exportGridState(), null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.download = `${randomGridName()}${GRID_FILE_EXTENSION}`;
  link.href = url;
  link.click();
  URL.revokeObjectURL(url);
});

const importGridInput = document.getElementById("importGridInput");

document.getElementById("importGridBtn").addEventListener("click", () => {
  importGridInput.click();
});

importGridInput.addEventListener("change", () => {
  const file = importGridInput.files[0];
  if (!file) return;
  // The accept=".tcgrid" attribute is only a hint to the OS file picker --
  // still enforce it here in case a file was picked some other way (e.g.
  // "all files" was chosen anyway, or the file was dropped in).
  if (!file.name.toLowerCase().endsWith(GRID_FILE_EXTENSION)) {
    statusEl.className = "error";
    statusEl.textContent = `Please select a ${GRID_FILE_EXTENSION} grid file.`;
    importGridInput.value = "";
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    try {
      importGridState(JSON.parse(reader.result));
      statusEl.className = "ok";
      statusEl.textContent = "Grid imported.";
    } catch (err) {
      statusEl.className = "error";
      statusEl.textContent = "Could not read that file: " + err;
    }
    importGridInput.value = "";
  };
  reader.readAsText(file);
});
