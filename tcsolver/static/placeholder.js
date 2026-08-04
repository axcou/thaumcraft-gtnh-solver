const packsEl = document.getElementById("packs");

async function init() {
  const resp = await fetch("/aspects");
  const aspectData = await resp.json();
  renderPackSelector(packsEl, aspectData, null);
}

init();
