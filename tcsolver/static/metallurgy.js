// Metallurgic Perfection page: one row per metal, listing how many of
// which aspects its nugget needs (from tcsolver/metallurgy.py), searchable
// by metal name and restricted to the currently active mod packs.

const searchBox = document.getElementById("searchBox");
const metallurgyBody = document.getElementById("metallurgyBody");
const packsEl = document.getElementById("packs");

let aspectData = { aspects: {}, flavor: {}, packs: {}, default_packs: [], metallurgy: [] };
let packSelector = null;

function makeRequirementChip(req) {
  const chip = document.createElement("span");
  chip.className = "req-chip";
  const img = document.createElement("img");
  img.src = `/static/icons/${req.aspect}.svg`;
  const label = document.createElement("span");
  label.textContent = `${req.amount}× ${capitalize(req.aspect)}`;
  chip.appendChild(img);
  chip.appendChild(label);
  return chip;
}

function makeRow(recipe) {
  const row = document.createElement("tr");

  const metalCell = document.createElement("td");
  metalCell.className = "metal-name";
  metalCell.textContent = recipe.metal;
  row.appendChild(metalCell);

  const reqCell = document.createElement("td");
  reqCell.className = "req-list";
  for (const req of recipe.requires) {
    reqCell.appendChild(makeRequirementChip(req));
  }
  row.appendChild(reqCell);

  return row;
}

function renderTable() {
  const packs = packSelector.checkedPacks();
  const enabled = new Set();
  for (const p of packs) {
    for (const a of aspectData.packs[p] || []) enabled.add(a);
  }
  const filterText = searchBox.value.trim().toLowerCase();

  const recipes = aspectData.metallurgy
    .filter((r) => r.requires.every((req) => enabled.has(req.aspect)))
    .filter((r) => !filterText || r.metal.toLowerCase().includes(filterText));

  metallurgyBody.innerHTML = "";
  for (const recipe of recipes) {
    metallurgyBody.appendChild(makeRow(recipe));
  }

  if (recipes.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 2;
    cell.className = "empty-hint";
    cell.textContent = "No metals match the current filters.";
    row.appendChild(cell);
    metallurgyBody.appendChild(row);
  }
}

searchBox.addEventListener("input", renderTable);

async function init() {
  const resp = await fetch("/aspects");
  aspectData = await resp.json();
  packSelector = renderPackSelector(packsEl, aspectData, renderTable);
  renderTable();
}

init();
