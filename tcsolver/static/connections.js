const statusEl = document.getElementById("status");
const packsEl = document.getElementById("packs");
const fromSelect = document.getElementById("fromSelect");
const toSelect = document.getElementById("toSelect");
const minSteps = document.getElementById("minSteps");
const resultChain = document.getElementById("resultChain");
const stepBadge = document.getElementById("stepBadge");
const hoverBreakdown = document.getElementById("hoverBreakdown");

let aspectData = { aspects: {}, flavor: {}, packs: {}, default_packs: [], complexity: {} };
let packSelector = null;

// capitalize() and makeComboIcon() come from utils.js.

function populateAspectSelects() {
  const names = Object.keys(aspectData.aspects).sort((a, b) => a.localeCompare(b));
  for (const select of [fromSelect, toSelect]) {
    select.innerHTML = "";
    for (const aspect of names) {
      const opt = document.createElement("option");
      opt.value = aspect;
      const flavor = aspectData.flavor[aspect];
      opt.textContent = flavor ? `${capitalize(aspect)} (${flavor})` : capitalize(aspect);
      select.appendChild(opt);
    }
  }
  fromSelect.value = "aer";
  toSelect.value = "ignis";
}

// "A + B = aspect" (or "Primal aspect" if it has no components), shown
// below the chain while hovering one of its aspects, so it's clear why
// that particular aspect was picked to link its neighbors.
function renderBreakdown(aspect) {
  hoverBreakdown.innerHTML = "";
  const components = aspectData.aspects[aspect] || [];
  const card = document.createElement("div");
  card.className = "combo-card";

  if (components.length === 0) {
    const primal = document.createElement("div");
    primal.className = "combo-primal";
    primal.textContent = `${capitalize(aspect)} is a primal aspect.`;
    card.appendChild(primal);
  } else {
    const comps = document.createElement("div");
    comps.className = "combo-components";
    components.forEach((comp, index) => {
      comps.appendChild(makeComboIcon(comp, "combo-component"));
      if (index < components.length - 1) {
        const plus = document.createElement("span");
        plus.className = "combo-plus";
        plus.textContent = "+";
        comps.appendChild(plus);
      }
    });
    card.appendChild(comps);
    const equals = document.createElement("div");
    equals.className = "combo-equals";
    equals.textContent = "=";
    card.appendChild(equals);
    card.appendChild(makeComboIcon(aspect, "combo-result"));
  }

  hoverBreakdown.appendChild(card);
}

function clearBreakdown() {
  hoverBreakdown.innerHTML = "";
  hoverBreakdown.style.display = "none";
}

// Keeps the floating breakdown box glued near the cursor as it moves.
function positionBreakdown(evt) {
  hoverBreakdown.style.left = `${evt.clientX + 16}px`;
  hoverBreakdown.style.top = `${evt.clientY - 70}px`;
}

function renderChainItem(aspect) {
  const item = makeComboIcon(aspect, "chain-item");
  item.addEventListener("mouseenter", (evt) => {
    renderBreakdown(aspect);
    hoverBreakdown.style.display = "block";
    positionBreakdown(evt);
  });
  item.addEventListener("mousemove", positionBreakdown);
  item.addEventListener("mouseleave", clearBreakdown);
  return item;
}

function clearResult() {
  resultChain.innerHTML = "";
  stepBadge.textContent = "";
  clearBreakdown();
}

function renderResult(path) {
  resultChain.innerHTML = "";
  path.forEach((aspect, index) => {
    resultChain.appendChild(renderChainItem(aspect));
    if (index < path.length - 1) {
      const arrow = document.createElement("span");
      arrow.className = "chain-arrow";
      arrow.textContent = "→";
      resultChain.appendChild(arrow);
    }
  });

  const steps = path.length - 1;
  stepBadge.textContent = `${steps} step${steps === 1 ? "" : "s"}`;
}

document.getElementById("findBtn").addEventListener("click", async () => {
  statusEl.className = "";
  statusEl.textContent = "Searching...";
  clearResult();
  const payload = {
    from: fromSelect.value,
    to: toSelect.value,
    min_steps: parseInt(minSteps.value, 10) || 1,
    packs: packSelector.checkedPacks(),
  };
  try {
    const resp = await fetch("/connect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await resp.json();
    if (data.success) {
      renderResult(data.path);
      // The chain itself is the result -- a redundant "Connection found."
      // line added nothing and, since #connectionControls centers its
      // content vertically, shifted the whole column every time it
      // appeared/disappeared.
      statusEl.className = "";
      statusEl.textContent = "";
    } else {
      statusEl.className = "error";
      statusEl.textContent = data.message || "No connection found.";
    }
  } catch (err) {
    statusEl.className = "error";
    statusEl.textContent = "Could not reach the server: " + err;
  }
});

async function init() {
  const resp = await fetch("/aspects");
  aspectData = await resp.json();
  packSelector = renderPackSelector(packsEl, aspectData, null);
  packSelector.applyPreset(); // Connection Helper defaults to the GTNH pack set.
  populateAspectSelects();
}

init();
