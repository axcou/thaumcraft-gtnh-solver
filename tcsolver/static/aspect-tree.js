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

const X_UNIT = 86; // horizontal slot width -- just wider than the widest tree-box (~78px)
const Y_UNIT = 76; // vertical distance between levels
const SVG_NS = "http://www.w3.org/2000/svg";

// Assigns every node an integer x "slot" and a depth, bottom-up: each leaf
// (primal aspect) takes the next free slot, and each parent sits at the
// *average* of its own two children's slots -- not, as a naive nested-flex
// layout would, at the center of their combined subtree width. That's what
// keeps a childless leaf close to its parent even when its sibling has a
// much deeper subtree, instead of being dragged out to balance it.
// Every non-primal aspect here has exactly 2 components, so this never
// needs to special-case a lone child.
function layoutTree(aspect) {
  const nodes = [];
  let nextLeafSlot = 0;

  function visit(name, depth, parentIndex) {
    const index = nodes.length;
    nodes.push({ aspect: name, depth, parentIndex, x: 0 });
    const components = aspectData.aspects[name] || [];
    if (components.length === 0) {
      nodes[index].x = nextLeafSlot++;
    } else {
      const childIndexes = components.map((comp) => visit(comp, depth + 1, index));
      const xs = childIndexes.map((ci) => nodes[ci].x);
      nodes[index].x = (xs[0] + xs[1]) / 2;
    }
    return index;
  }

  visit(aspect, 0, -1);
  return nodes;
}

function renderTree(aspect) {
  treeDiagram.innerHTML = "";
  const nodes = layoutTree(aspect);

  let maxX = 0;
  let maxDepth = 0;
  for (const node of nodes) {
    maxX = Math.max(maxX, node.x);
    maxDepth = Math.max(maxDepth, node.depth);
  }
  const width = (maxX + 1) * X_UNIT;
  const height = (maxDepth + 1) * Y_UNIT;
  treeDiagram.style.width = `${width}px`;
  treeDiagram.style.height = `${height}px`;

  const elements = nodes.map((node) => {
    const el = document.createElement("div");
    el.className = "tree-node";
    el.style.left = `${(node.x + 0.5) * X_UNIT}px`;
    el.style.top = `${(node.depth + 0.5) * Y_UNIT}px`;
    el.appendChild(makeComboIcon(node.aspect, "tree-box"));
    treeDiagram.appendChild(el);
    return el;
  });

  // Connectors need each box's *actual* rendered edges (its height varies
  // slightly with font rendering) for the lines to land exactly on them,
  // so they're measured only after the boxes above are already in the DOM.
  const diagramRect = treeDiagram.getBoundingClientRect();
  const edges = elements.map((el) => {
    const r = el.getBoundingClientRect();
    return {
      centerX: r.x + r.width / 2 - diagramRect.x,
      top: r.y - diagramRect.y,
      bottom: r.y + r.height - diagramRect.y,
    };
  });

  const svg = document.createElementNS(SVG_NS, "svg");
  svg.setAttribute("class", "tree-connectors");
  svg.setAttribute("width", width);
  svg.setAttribute("height", height);

  // Group children by their parent -- every parent here has exactly 2.
  const childrenByParent = new Map();
  nodes.forEach((node, index) => {
    if (node.parentIndex < 0) return;
    if (!childrenByParent.has(node.parentIndex)) childrenByParent.set(node.parentIndex, []);
    childrenByParent.get(node.parentIndex).push(index);
  });

  for (const [parentIndex, childIndexes] of childrenByParent) {
    const parent = edges[parentIndex];
    const [c1, c2] = childIndexes.map((i) => edges[i]);
    const midY = parent.bottom + (c1.top - parent.bottom) / 2;
    const path = document.createElementNS(SVG_NS, "path");
    path.setAttribute(
      "d",
      `M ${parent.centerX} ${parent.bottom} L ${parent.centerX} ${midY} ` +
        `M ${c1.centerX} ${midY} L ${c2.centerX} ${midY} ` +
        `M ${c1.centerX} ${midY} L ${c1.centerX} ${c1.top} ` +
        `M ${c2.centerX} ${midY} L ${c2.centerX} ${c2.top}`
    );
    svg.appendChild(path);
  }

  treeDiagram.insertBefore(svg, treeDiagram.firstChild);
  resetView();
}
