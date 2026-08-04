// Hex board model, geometry, and canvas rendering for the Research Table
// Solver page. Board *interactions* (click / drag-drop) and grid import/
// export live in grid-io.js; the draggable aspect palette lives in
// aspect-palette.js; page wiring (size/clear/solve) lives in solver.js.

const HEX_SIZE = 28;
const PADDING = 40;
const MAX_RADIUS = 5; // biggest selectable size (6) - 1; the canvas / grid
// background always sizes for this, so it never changes as the board size
// changes, and the (smaller) grid just sits centered inside it.

const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

let radius = 4; // radius = size - 1
/** Map "q,r" -> {aspect: string|null, barred: bool, base: bool, solved: bool} */
let cells = new Map();
const iconCache = new Map();

function key(q, r) {
  return q + "," + r;
}

function getIcon(aspect) {
  let img = iconCache.get(aspect);
  if (!img) {
    img = new Image();
    img.src = `/static/icons/${aspect}.svg`;
    img.onload = () => draw();
    iconCache.set(aspect, img);
  }
  return img;
}

function buildBoard(newRadius) {
  radius = newRadius;
  cells = new Map();
  for (let q = -radius; q <= radius; q++) {
    const rLo = Math.max(-radius, -q - radius);
    const rHi = Math.min(radius, -q + radius);
    for (let r = rLo; r <= rHi; r++) {
      cells.set(key(q, r), { aspect: null, barred: false, base: false, solved: false });
    }
  }
  resizeCanvas();
  draw();
}

function resizeCanvas() {
  // Flat-top layout: hexagons are wider along q, taller along r. Always
  // sized for MAX_RADIUS, so the background stays constant and smaller
  // boards are simply centered within it (axialToPixel centers on
  // canvas.width/2, canvas.height/2 regardless of the current radius).
  const w = HEX_SIZE * 1.5 * (2 * MAX_RADIUS + 1) + PADDING * 2;
  const h = HEX_SIZE * Math.sqrt(3) * (2 * MAX_RADIUS + 1) + PADDING * 2;
  canvas.width = Math.ceil(w);
  canvas.height = Math.ceil(h);
}

// Flat-top axial-to-pixel (board rotated 90 deg relative to the usual
// pointy-top layout: points face left/right, flat edges face up/down).
function axialToPixel(q, r) {
  const x = HEX_SIZE * 1.5 * q + canvas.width / 2;
  const y = HEX_SIZE * Math.sqrt(3) * (r + q / 2) + canvas.height / 2;
  return [x, y];
}

function hexCorners(cx, cy) {
  const pts = [];
  for (let i = 0; i < 6; i++) {
    const angle = (Math.PI / 180) * (60 * i);
    pts.push([cx + HEX_SIZE * Math.cos(angle), cy + HEX_SIZE * Math.sin(angle)]);
  }
  return pts;
}

function drawHex(cx, cy, fill, stroke, lineWidth) {
  const pts = hexCorners(cx, cy);
  ctx.beginPath();
  ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
  ctx.closePath();
  if (fill) {
    ctx.fillStyle = fill;
    ctx.fill();
  }
  ctx.strokeStyle = stroke || "#555";
  ctx.lineWidth = lineWidth || 1.5;
  ctx.stroke();
}

function draw() {
  ctx.fillStyle = "#141516";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  for (const [k, cell] of cells) {
    const [q, r] = k.split(",").map(Number);
    const [cx, cy] = axialToPixel(q, r);
    if (cell.barred) {
      drawHex(cx, cy, "#000000", "#444", 1.5);
      continue;
    }
    let fill = "#1f2022";
    let stroke = "#4a4a4a";
    let lineWidth = 1.5;
    if (cell.aspect) {
      fill = "#2a2b2e";
      if (cell.base) {
        stroke = "#ffffff";
        lineWidth = 2.5;
      } else if (cell.solved) {
        stroke = "#ffd54a";
        lineWidth = 3;
      }
    }
    drawHex(cx, cy, fill, stroke, lineWidth);
    if (cell.aspect) {
      const icon = getIcon(cell.aspect);
      const size = HEX_SIZE * 1.3;
      if (icon.complete && icon.naturalWidth > 0) {
        ctx.drawImage(icon, cx - size / 2, cy - size / 2, size, size);
      }
    }
  }
}

function cellAtPixel(px, py) {
  let best = null;
  let bestDist = Infinity;
  for (const [k] of cells) {
    const [q, r] = k.split(",").map(Number);
    const [cx, cy] = axialToPixel(q, r);
    const d = Math.hypot(px - cx, py - cy);
    if (d < bestDist) {
      bestDist = d;
      best = k;
    }
  }
  if (best !== null && bestDist <= HEX_SIZE) return best;
  return null;
}

function eventToCanvasPixel(evt) {
  const rect = canvas.getBoundingClientRect();
  return [
    ((evt.clientX - rect.left) / rect.width) * canvas.width,
    ((evt.clientY - rect.top) / rect.height) * canvas.height,
  ];
}
