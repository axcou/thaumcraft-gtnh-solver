// Aspect list + search for the Aspect Combination page. The tree diagram
// and its pan/zoom (including renderTree(), called below) live in
// aspect-tree.js.

const searchBox = document.getElementById("searchBox");
const combinationList = document.getElementById("combinationList");
const packsEl = document.getElementById("packs");

let aspectData = { aspects: {}, flavor: {}, packs: {}, default_packs: [], complexity: {} };
let packSelector = null;
let selectedAspect = null;

function selectAspect(aspect) {
  selectedAspect = aspect;
  combinationList.querySelectorAll(".aspect-card").forEach((el) => {
    el.classList.toggle("selected", el.dataset.aspect === aspect);
  });
  renderTree(aspect);
}

// Each row is its own card: the aspect on top, "= A + B" (or "Primal
// aspect") right below it -- the composition is always visible, not
// hidden behind a hover/selection.
function makeAspectCard(aspect) {
  const card = document.createElement("div");
  card.className = "aspect-card";
  card.dataset.aspect = aspect;

  const main = document.createElement("div");
  main.className = "aspect-card-main";
  const img = document.createElement("img");
  img.src = `/static/icons/${aspect}.svg`;
  const name = document.createElement("span");
  name.textContent = capitalize(aspect);
  main.appendChild(img);
  main.appendChild(name);
  card.appendChild(main);

  const components = aspectData.aspects[aspect] || [];
  const recipe = document.createElement("div");
  if (components.length === 0) {
    recipe.className = "aspect-card-recipe combo-primal";
    recipe.textContent = "Primal aspect";
  } else {
    recipe.className = "aspect-card-recipe";
    const equals = document.createElement("span");
    equals.className = "combo-equals";
    equals.textContent = "=";
    recipe.appendChild(equals);
    components.forEach((comp, index) => {
      recipe.appendChild(makeComboIcon(comp, "combo-component"));
      if (index < components.length - 1) {
        const plus = document.createElement("span");
        plus.className = "combo-plus";
        plus.textContent = "+";
        recipe.appendChild(plus);
      }
    });
  }
  card.appendChild(recipe);

  card.addEventListener("click", () => selectAspect(aspect));
  return card;
}

function renderList() {
  const packs = packSelector.checkedPacks();
  const enabled = new Set();
  for (const p of packs) {
    for (const a of aspectData.packs[p] || []) enabled.add(a);
  }
  const filterText = searchBox.value.trim().toLowerCase();
  const names = Object.keys(aspectData.aspects)
    .filter((a) => enabled.has(a))
    .filter((a) => {
      if (!filterText) return true;
      const flavor = (aspectData.flavor[a] || "").toLowerCase();
      return a.includes(filterText) || flavor.includes(filterText);
    })
    .sort((a, b) => {
      const ca = aspectData.complexity[a] ?? 0;
      const cb = aspectData.complexity[b] ?? 0;
      return ca - cb || a.localeCompare(b);
    });

  combinationList.innerHTML = "";
  for (const aspect of names) {
    combinationList.appendChild(makeAspectCard(aspect));
  }

  if (names.length === 0) {
    selectedAspect = null;
    treeDiagram.innerHTML = "";
    return;
  }
  selectAspect(names.includes(selectedAspect) ? selectedAspect : names[0]);
}

searchBox.addEventListener("input", renderList);

async function init() {
  const resp = await fetch("/aspects");
  aspectData = await resp.json();
  packSelector = renderPackSelector(packsEl, aspectData, renderList);
  renderList();
}

init();
