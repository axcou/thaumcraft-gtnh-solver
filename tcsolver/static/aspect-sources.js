// Aspect Sources page: a card per aspect listing cheap/pure item sources
// (from tcsolver/sources.py), filterable by pure/especially-good and by
// aspect name, and restricted to the currently active mod packs.

const searchBox = document.getElementById("searchBox");
const pureOnlyCheckbox = document.getElementById("pureOnly");
const goodOnlyCheckbox = document.getElementById("goodOnly");
const sourcesGrid = document.getElementById("sourcesGrid");
const packsEl = document.getElementById("packs");

let aspectData = { aspects: {}, flavor: {}, packs: {}, default_packs: [], sources: {} };
let packSelector = null;

function entryMatchesFilters(entry) {
  const pureOnly = pureOnlyCheckbox.checked;
  const goodOnly = goodOnlyCheckbox.checked;
  if (!pureOnly && !goodOnly) return true;
  return (pureOnly && entry.impurity === 0) || (goodOnly && entry.highlight === "good");
}

function makeSourceCard(aspect, entries) {
  const card = document.createElement("div");
  card.className = "source-card";

  const header = document.createElement("div");
  header.className = "source-card-header";
  const img = document.createElement("img");
  img.src = `/static/icons/${aspect}.svg`;
  const name = document.createElement("span");
  name.textContent = capitalize(aspect);
  header.appendChild(img);
  header.appendChild(name);
  card.appendChild(header);

  const list = document.createElement("div");
  list.className = "source-list";
  for (const entry of entries) {
    const row = document.createElement("div");
    row.className = "source-item";
    if (entry.highlight === "good") row.classList.add("highlight-good");
    if (entry.highlight === "hard") row.classList.add("highlight-hard");

    const badge = document.createElement("span");
    badge.className = "impurity-badge";
    badge.textContent = entry.impurity === 0 ? "pure" : `+${entry.impurity}`;
    row.appendChild(badge);

    const text = document.createElement("span");
    text.className = "source-item-text";
    text.textContent = entry.item;
    row.appendChild(text);

    list.appendChild(row);
  }
  card.appendChild(list);
  return card;
}

function renderGrid() {
  const packs = packSelector.checkedPacks();
  const enabled = new Set();
  for (const p of packs) {
    for (const a of aspectData.packs[p] || []) enabled.add(a);
  }
  const filterText = searchBox.value.trim().toLowerCase();

  const aspectNames = Object.keys(aspectData.sources)
    .filter((a) => enabled.has(a))
    .filter((a) => {
      if (!filterText) return true;
      const flavor = (aspectData.flavor[a] || "").toLowerCase();
      return a.includes(filterText) || flavor.includes(filterText);
    })
    .sort((a, b) => a.localeCompare(b));

  sourcesGrid.innerHTML = "";
  let shown = 0;
  for (const aspect of aspectNames) {
    const entries = aspectData.sources[aspect].filter(entryMatchesFilters);
    if (entries.length === 0) continue;
    sourcesGrid.appendChild(makeSourceCard(aspect, entries));
    shown++;
  }

  if (shown === 0) {
    sourcesGrid.innerHTML = '<p class="empty-hint">No sources match the current filters.</p>';
  }
}

searchBox.addEventListener("input", renderGrid);
pureOnlyCheckbox.addEventListener("change", renderGrid);
goodOnlyCheckbox.addEventListener("change", renderGrid);

async function init() {
  const resp = await fetch("/aspects");
  aspectData = await resp.json();
  packSelector = renderPackSelector(packsEl, aspectData, renderGrid);
  renderGrid();
}

init();
