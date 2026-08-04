// Item Aspect Lookup page: searches the full GTNH item scan database
// (tcsolver/static/data/item_aspects.json, ~16k items) by name and/or by
// aspect, sorted purest (fewest total aspects) first, restricted to the
// currently active mod packs.

const searchBox = document.getElementById("searchBox");
const aspectFilter = document.getElementById("aspectFilter");
const resultCount = document.getElementById("resultCount");
const lookupBody = document.getElementById("lookupBody");
const packsEl = document.getElementById("packs");

const RESULT_CAP = 300;

let aspectData = { aspects: {}, flavor: {}, packs: {}, default_packs: [] };
let itemData = { aspects: [], items: [] };
let packSelector = null;

function populateAspectFilter() {
  const names = [...itemData.aspects].sort();
  for (const aspect of names) {
    const option = document.createElement("option");
    option.value = aspect;
    option.textContent = capitalize(aspect);
    aspectFilter.appendChild(option);
  }
}

function makeAspectChip(aspect, amount) {
  const chip = document.createElement("span");
  chip.className = "req-chip";
  const img = document.createElement("img");
  img.src = `/static/icons/${aspect}.svg`;
  const label = document.createElement("span");
  label.textContent = `${amount}× ${capitalize(aspect)}`;
  chip.appendChild(img);
  chip.appendChild(label);
  return chip;
}

function makeRow(item) {
  const row = document.createElement("tr");

  const nameCell = document.createElement("td");
  nameCell.className = "metal-name";
  nameCell.textContent = item.name;
  row.appendChild(nameCell);

  const aspectsCell = document.createElement("td");
  aspectsCell.className = "req-list";
  for (const [aspect, amount] of Object.entries(item.aspects)) {
    aspectsCell.appendChild(makeAspectChip(aspect, amount));
  }
  row.appendChild(aspectsCell);

  return row;
}

function renderTable() {
  const packs = packSelector.checkedPacks();
  const enabled = new Set();
  for (const p of packs) {
    for (const a of aspectData.packs[p] || []) enabled.add(a);
  }
  const filterText = searchBox.value.trim().toLowerCase();
  const wantedAspect = aspectFilter.value;

  const matches = itemData.items
    .filter((it) => !filterText || it.name.toLowerCase().includes(filterText))
    .filter((it) => !wantedAspect || wantedAspect in it.aspects)
    .filter((it) => Object.keys(it.aspects).every((a) => enabled.has(a)))
    .sort((a, b) => {
      const na = Object.keys(a.aspects).length;
      const nb = Object.keys(b.aspects).length;
      return na - nb || a.name.localeCompare(b.name);
    });

  const shown = matches.slice(0, RESULT_CAP);

  lookupBody.innerHTML = "";
  for (const item of shown) {
    lookupBody.appendChild(makeRow(item));
  }

  if (matches.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 2;
    cell.className = "empty-hint";
    cell.textContent = "No items match the current filters.";
    row.appendChild(cell);
    lookupBody.appendChild(row);
    resultCount.textContent = "";
  } else if (matches.length > RESULT_CAP) {
    resultCount.textContent = `Showing ${RESULT_CAP} of ${matches.length} matches -- refine your search.`;
  } else {
    resultCount.textContent = `${matches.length} match${matches.length === 1 ? "" : "es"}`;
  }
}

searchBox.addEventListener("input", renderTable);
aspectFilter.addEventListener("change", renderTable);

async function init() {
  const [aspectsResp, itemsResp] = await Promise.all([
    fetch("/aspects"),
    fetch("/static/data/item_aspects.json"),
  ]);
  aspectData = await aspectsResp.json();
  itemData = await itemsResp.json();
  populateAspectFilter();
  packSelector = renderPackSelector(packsEl, aspectData, renderTable);
  renderTable();
}

init();
