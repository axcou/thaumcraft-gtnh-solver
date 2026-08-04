// The draggable aspect palette (the two side columns on the Solver page).
// Needs `aspectData` and `packSelector`, set up by solver.js's init().

const aspectsLeft = document.getElementById("aspectsLeft");
const aspectsRight = document.getElementById("aspectsRight");

function makeAspectItem(aspect) {
  const item = document.createElement("div");
  item.className = "aspect-icon";
  item.draggable = true;
  const flavor = aspectData.flavor[aspect] || "";
  item.title = flavor ? `${capitalize(aspect)} (${flavor})` : capitalize(aspect);
  const img = document.createElement("img");
  img.src = `/static/icons/${aspect}.svg`;
  const span = document.createElement("span");
  span.textContent = capitalize(aspect);
  item.appendChild(img);
  item.appendChild(span);
  item.addEventListener("dragstart", (evt) => {
    evt.dataTransfer.setData("text/plain", aspect);
    // Drag a standalone clone of just the icon, not the tile: dragging the
    // original <img> in place can pull in the tile's gray square backdrop
    // as part of the browser's drag-image snapshot. A clone sitting off
    // -screen on its own has no such backdrop to inherit.
    const ghost = img.cloneNode();
    ghost.style.position = "fixed";
    ghost.style.top = "-999px";
    ghost.style.left = "-999px";
    ghost.style.width = "40px";
    ghost.style.height = "40px";
    ghost.style.background = "transparent";
    document.body.appendChild(ghost);
    evt.dataTransfer.setDragImage(ghost, 20, 20);
    item._dragGhost = ghost;
    item.classList.add("dragging");
  });
  item.addEventListener("dragend", () => {
    item.classList.remove("dragging");
    if (item._dragGhost) {
      item._dragGhost.remove();
      item._dragGhost = null;
    }
  });
  return item;
}

function renderAspectPalette() {
  const packs = packSelector.checkedPacks();
  const enabled = new Set();
  for (const p of packs) {
    for (const a of aspectData.packs[p] || []) enabled.add(a);
  }
  // Simplest (fewest crafting steps) aspects first, alphabetical among ties.
  const options = Array.from(enabled).sort((a, b) => {
    const ca = aspectData.complexity[a] ?? 0;
    const cb = aspectData.complexity[b] ?? 0;
    return ca - cb || a.localeCompare(b);
  });

  aspectsLeft.innerHTML = "";
  aspectsRight.innerHTML = "";
  const half = Math.ceil(options.length / 2);
  options.slice(0, half).forEach((aspect) => aspectsLeft.appendChild(makeAspectItem(aspect)));
  options.slice(half).forEach((aspect) => aspectsRight.appendChild(makeAspectItem(aspect)));
}
