// Tiny helpers shared by every page's script. Load this before any other
// page script that uses them.

function capitalize(name) {
  return name.charAt(0).toUpperCase() + name.slice(1);
}

// A small "icon + name" tile: the aspect palette, the Connection Helper's
// chain/breakdown, and the Aspect Combination page's cards/tree all build
// this same shape, just under different classNames.
function makeComboIcon(aspect, className) {
  const wrap = document.createElement("div");
  wrap.className = className;
  const img = document.createElement("img");
  img.src = `/static/icons/${aspect}.svg`;
  const span = document.createElement("span");
  span.textContent = capitalize(aspect);
  wrap.appendChild(img);
  wrap.appendChild(span);
  return wrap;
}
