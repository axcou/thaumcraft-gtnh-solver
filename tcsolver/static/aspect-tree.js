// Pan & zoom (wheel = zoom, drag = pan) and the recursive tree-diagram
// builder for the Aspect Combination page. The aspect list / search UI
// and page init live in combinations.js, which calls renderTree().

const treeWrapper = document.getElementById("treeWrapper");
const treeDiagram = document.getElementById("treeDiagram");

const MIN_ZOOM = 0.25;
const MAX_ZOOM = 2.5;
let zoom = 1;
let panX = 0;
let panY = 0;

function applyTransform() {
  treeDiagram.style.transform = `translate(${panX}px, ${panY}px) scale(${zoom})`;
}

// Resets zoom to 1:1 and re-centers the (possibly newly rendered, and so
// differently sized) diagram in the middle of the viewport.
function resetView() {
  zoom = 1;
  panX = 0;
  panY = 0;
  applyTransform();
  const wrapperRect = treeWrapper.getBoundingClientRect();
  const diagramRect = treeDiagram.getBoundingClientRect();
  panX = Math.round((wrapperRect.width - diagramRect.width) / 2);
  panY = Math.round((wrapperRect.height - diagramRect.height) / 2);
  applyTransform();
}

treeWrapper.addEventListener("wheel", (evt) => {
  evt.preventDefault();
  const rect = treeWrapper.getBoundingClientRect();
  const mouseX = evt.clientX - rect.left;
  const mouseY = evt.clientY - rect.top;
  const factor = evt.deltaY < 0 ? 1.1 : 1 / 1.1;
  const newZoom = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, zoom * factor));
  // Keep the diagram point under the cursor fixed while the scale changes.
  panX = mouseX - ((mouseX - panX) / zoom) * newZoom;
  panY = mouseY - ((mouseY - panY) / zoom) * newZoom;
  zoom = newZoom;
  applyTransform();
});

let dragging = false;
let dragStartX = 0;
let dragStartY = 0;
let panStartX = 0;
let panStartY = 0;

treeWrapper.addEventListener("mousedown", (evt) => {
  dragging = true;
  dragStartX = evt.clientX;
  dragStartY = evt.clientY;
  panStartX = panX;
  panStartY = panY;
  treeWrapper.classList.add("dragging");
});

window.addEventListener("mousemove", (evt) => {
  if (!dragging) return;
  panX = panStartX + (evt.clientX - dragStartX);
  panY = panStartY + (evt.clientY - dragStartY);
  applyTransform();
});

window.addEventListener("mouseup", () => {
  if (!dragging) return;
  dragging = false;
  treeWrapper.classList.remove("dragging");
});

// Recursively builds the <li> for `aspect`, with a nested <ul> of its
// components (which are themselves built the same way) when it's not a
// primal aspect. Every non-primal aspect here has exactly 2 components, so
// this never needs to special-case a single child.
function buildTreeNode(aspect) {
  const li = document.createElement("li");
  li.appendChild(makeComboIcon(aspect, "tree-box"));
  const components = aspectData.aspects[aspect] || [];
  if (components.length > 0) {
    const ul = document.createElement("ul");
    components.forEach((comp) => ul.appendChild(buildTreeNode(comp)));
    li.appendChild(ul);
  }
  return li;
}

function renderTree(aspect) {
  treeDiagram.innerHTML = "";
  const ul = document.createElement("ul");
  ul.appendChild(buildTreeNode(aspect));
  treeDiagram.appendChild(ul);
  resetView();
}
