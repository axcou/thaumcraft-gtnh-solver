// Shared "Active mods" widget, used by every page: a GTNH preset button
// plus one checkbox per pack. Included as a plain <script> before each
// page's own script, which calls renderPackSelector(...).

const GTNH_PRESET = ["vanilla_tc", "gregtech", "forbidden_magic", "magic_bees"];

function renderPackSelector(container, aspectData, onChange) {
  container.innerHTML = "";

  const presetBtn = document.createElement("button");
  presetBtn.type = "button";
  presetBtn.className = "secondary";
  presetBtn.textContent = "GTNH preset";
  container.appendChild(presetBtn);

  const list = document.createElement("div");
  list.className = "packs-list";
  container.appendChild(list);

  for (const packName of Object.keys(aspectData.packs)) {
    const id = "pack_" + packName;
    const label = document.createElement("label");
    const checked = aspectData.default_packs.includes(packName) ? "checked" : "";
    label.innerHTML = `<input type="checkbox" id="${id}" value="${packName}" ${checked} /> ${packName}`;
    list.appendChild(label);
  }

  function checkedPacks() {
    return Array.from(list.querySelectorAll("input[type=checkbox]:checked")).map((el) => el.value);
  }

  function applyPreset() {
    setPacks(GTNH_PRESET);
  }

  // Checks exactly the given packs (used when restoring an imported grid).
  function setPacks(names) {
    list.querySelectorAll("input[type=checkbox]").forEach((el) => {
      el.checked = names.includes(el.value);
    });
    if (onChange) onChange(checkedPacks());
  }

  list.addEventListener("change", () => {
    if (onChange) onChange(checkedPacks());
  });

  presetBtn.addEventListener("click", applyPreset);

  return { checkedPacks, applyPreset, setPacks };
}
