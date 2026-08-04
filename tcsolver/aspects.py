"""Aspect combination table for Thaumcraft + GTNH addons.

Ported verbatim from `aspect_table` (lines 855-930) and `aspect_set` (lines
971-982) in SkilledAlpaca/universal_tc_research_solver's index.html, which
already curates a set relevant to GTNH (vanilla Thaumcraft + Forbidden Magic
+ Gregtech + Magic Bees + Avaritia + a few extra GT:NH-side mods).

The 7 Thaumic Tinkerer aspects (aequalitas, primordium, astrum, caelum,
gloria, tabernus, vesania) were missing from that port and were added from
the "TC (Aspects)" tab of a GTNH guide spreadsheet
(https://docs.google.com/spreadsheets/d/1rsB5OOAkFgJ_lzhtVzWZc2aNCSo0e6lRhJG8Po7NZtY);
5 of the 7 are also directly referenced by name in GTNH's own GregTech
source (`TCAspects.java`), confirming they're live aspects in the pack.

Each compound aspect lists its exactly-2 direct components; primal aspects
have an empty list.
"""

from __future__ import annotations

from typing import Dict, FrozenSet, Iterable, List, Set

ASPECT_TABLE: Dict[str, List[str]] = {
    # --- vanilla Thaumcraft (48) ---
    "aer": [],
    "alienis": ["vacuos", "tenebrae"],
    "aqua": [],
    "arbor": ["aer", "herba"],
    "auram": ["aer", "praecantatio"],
    "bestia": ["motus", "victus"],
    "cognitio": ["ignis", "spiritus"],
    "corpus": ["bestia", "mortuus"],
    "exanimis": ["motus", "mortuus"],
    "fabrico": ["humanus", "instrumentum"],
    "fames": ["vacuos", "victus"],
    "gelum": ["ignis", "perditio"],
    "herba": ["terra", "victus"],
    "humanus": ["bestia", "cognitio"],
    "ignis": [],
    "instrumentum": ["ordo", "humanus"],
    "iter": ["terra", "motus"],
    "limus": ["aqua", "victus"],
    "lucrum": ["fames", "humanus"],
    "lux": ["aer", "ignis"],
    "machina": ["motus", "instrumentum"],
    "messis": ["herba", "humanus"],
    "metallum": ["terra", "vitreus"],
    "meto": ["instrumentum", "messis"],
    "mortuus": ["perditio", "victus"],
    "motus": ["aer", "ordo"],
    "ordo": [],
    "pannus": ["bestia", "instrumentum"],
    "perditio": [],
    "perfodio": ["terra", "humanus"],
    "permutatio": ["ordo", "perditio"],
    "potentia": ["ignis", "ordo"],
    "praecantatio": ["potentia", "vacuos"],
    "sano": ["ordo", "victus"],
    "sensus": ["aer", "spiritus"],
    "spiritus": ["victus", "mortuus"],
    "telum": ["ignis", "instrumentum"],
    "tempestas": ["aer", "aqua"],
    "tenebrae": ["lux", "vacuos"],
    "terra": [],
    "tutamen": ["terra", "instrumentum"],
    "vacuos": ["aer", "perditio"],
    "venenum": ["aqua", "perditio"],
    "victus": ["aqua", "terra"],
    "vinculum": ["perditio", "motus"],
    "vitium": ["perditio", "praecantatio"],
    "vitreus": ["ordo", "terra"],
    "volatus": ["aer", "motus"],
    # --- Forbidden Magic (7) / Gregtech (5) / Magic Bees (1) / Avaritia (1) ---
    "desidia": ["vinculum", "spiritus"],
    "gula": ["fames", "vacuos"],
    "infernus": ["ignis", "praecantatio"],
    "invidia": ["sensus", "fames"],
    "ira": ["telum", "ignis"],
    "luxuria": ["corpus", "fames"],
    "superbia": ["volatus", "vacuos"],
    "tempus": ["vacuos", "ordo"],
    "electrum": ["potentia", "machina"],
    "magneto": ["metallum", "iter"],
    "nebrisum": ["perfodio", "lucrum"],
    "radio": ["lux", "potentia"],
    "strontio": ["perditio", "cognitio"],
    "terminus": ["alienis", "lucrum"],
    # --- other GT:NH-relevant additions (10) ---
    "coralos": ["venenum", "aqua"],
    "dreadia": ["venenum", "ignis"],
    "tincturem": ["lux", "ordo"],
    "sanctus": ["spiritus", "auram"],
    "exubitor": ["alienis", "mortuus"],
    "saxum": ["terra", "terra"],
    "granum": ["terra", "victus"],
    "mru": ["praecantatio", "potentia"],
    "radiation": ["mru", "motus"],
    "matrix": ["mru", "humanus"],
    # --- Thaumic Tinkerer (7) ---
    "aequalitas": ["cognitio", "ordo"],
    "primordium": ["motus", "vacuos"],
    "astrum": ["lux", "primordium"],
    "caelum": ["vitreus", "metallum"],
    "gloria": ["humanus", "iter"],
    "tabernus": ["tutamen", "iter"],
    "vesania": ["cognitio", "vitium"],
}

# English display flavor for each aspect id (from aspect_flavor_dict).
FLAVOR: Dict[str, str] = {
    "aer": "air",
    "alienis": "eldritch",
    "aqua": "water",
    "arbor": "tree",
    "auram": "aura",
    "bestia": "beast",
    "cognitio": "mind",
    "corpus": "flesh",
    "exanimis": "undead",
    "fabrico": "craft",
    "fames": "hunger",
    "gelum": "cold",
    "herba": "plant",
    "humanus": "man",
    "ignis": "fire",
    "instrumentum": "tool",
    "iter": "travel",
    "limus": "slime",
    "lucrum": "desire",
    "lux": "light",
    "machina": "mechanism",
    "messis": "crop",
    "metallum": "metal",
    "meto": "harvest",
    "mortuus": "death",
    "motus": "motion",
    "ordo": "order",
    "pannus": "cloth",
    "perditio": "entropy",
    "perfodio": "mine",
    "permutatio": "exchange",
    "potentia": "energy",
    "praecantatio": "magic",
    "sano": "health",
    "sensus": "senses",
    "spiritus": "soul",
    "telum": "weapon",
    "tempestas": "weather",
    "tenebrae": "darkness",
    "terra": "earth",
    "tutamen": "armor",
    "vacuos": "void",
    "venenum": "poison",
    "victus": "life",
    "vinculum": "trap",
    "vitium": "taint",
    "vitreus": "crystal",
    "volatus": "flight",
    "desidia": "sloth",
    "gula": "gluttony",
    "infernus": "nether",
    "invidia": "envy",
    "ira": "wrath",
    "luxuria": "lust",
    "superbia": "pride",
    "tempus": "time",
    "electrum": "electricity",
    "magneto": "magnetism",
    "nebrisum": "cheatiness",
    "radio": "radioactivity",
    "strontio": "stupidity",
    "terminus": "apocalypse",
    "coralos": "coralium",
    "dreadia": "dread",
    "tincturem": "color",
    "sanctus": "holiness",
    "exubitor": "warden",
    "saxum": "stone",
    "granum": "seed",
    "mru": "magical radiation unit",
    "radiation": "radiation",
    "matrix": "protection",
    "aequalitas": "equality",
    "primordium": "genesis",
    "astrum": "star",
    "caelum": "sky",
    "gloria": "glory",
    "tabernus": "shelter",
    "vesania": "insanity",
}

# Aspect packs, mirroring `aspect_set` in the reference solver.
PACKS: Dict[str, List[str]] = {
    "vanilla_tc": [
        "aer", "alienis", "aqua", "arbor", "auram", "bestia", "cognitio",
        "corpus", "exanimis", "fabrico", "fames", "gelum", "herba", "humanus",
        "ignis", "instrumentum", "iter", "limus", "lucrum", "lux", "machina",
        "messis", "metallum", "meto", "mortuus", "motus", "ordo", "pannus",
        "perditio", "perfodio", "permutatio", "potentia", "praecantatio",
        "sano", "sensus", "spiritus", "telum", "tempestas", "tenebrae",
        "terra", "tutamen", "vacuos", "venenum", "victus", "vinculum",
        "vitium", "vitreus", "volatus",
    ],
    "forbidden_magic": ["desidia", "gula", "infernus", "invidia", "ira", "luxuria", "superbia"],
    "gregtech": ["electrum", "magneto", "nebrisum", "radio", "strontio"],
    "magic_bees": ["tempus"],
    "avaritia": ["terminus"],
    "abyssal": ["coralos", "dreadia"],
    "botanical": ["tincturem"],
    "elysium": ["sanctus"],
    "revelations": ["exubitor"],
    "additions": ["saxum", "granum"],
    "essential": ["mru", "radiation", "matrix"],
    "thaumic_tinkerer": [
        "aequalitas", "primordium", "astrum", "caelum", "gloria", "tabernus", "vesania",
    ],
}

# The GTNH preset (see packs.js's GTNH_PRESET) doubles as the default
# selection on every page's first load.
DEFAULT_PACKS: List[str] = ["vanilla_tc", "gregtech", "forbidden_magic", "magic_bees"]

ALL_ASPECTS: FrozenSet[str] = frozenset(ASPECT_TABLE)


def components(aspect: str) -> List[str]:
    """The 0 or 2 direct components of `aspect`."""
    return ASPECT_TABLE[aspect]


def _build_adjacency() -> Dict[str, FrozenSet[str]]:
    adjacency: Dict[str, Set[str]] = {name: set() for name in ASPECT_TABLE}
    for aspect, comps in ASPECT_TABLE.items():
        for comp in comps:
            adjacency[aspect].add(comp)
            adjacency[comp].add(aspect)
    return {name: frozenset(neighbors) for name, neighbors in adjacency.items()}


# For each aspect, the set of aspects directly connectable to it (its 0-2
# components, plus every aspect that has it as a component).
ADJACENCY: Dict[str, FrozenSet[str]] = _build_adjacency()


def can_connect(a: str, b: str) -> bool:
    """True if `a` and `b` may sit on adjacent research-table hexes."""
    return b in ADJACENCY[a]


def enabled_aspects(pack_names: Iterable[str]) -> Set[str]:
    """The set of aspect ids enabled by the given packs."""
    enabled: Set[str] = set()
    for pack in pack_names:
        enabled.update(PACKS.get(pack, ()))
    return enabled


def _build_complexity() -> Dict[str, int]:
    """Number of crafting steps needed to reach each aspect: 0 for primal
    aspects, 1 + the harder of its two components otherwise."""
    memo: Dict[str, int] = {}

    def depth(aspect: str) -> int:
        if aspect in memo:
            return memo[aspect]
        comps = ASPECT_TABLE[aspect]
        value = 0 if not comps else 1 + max(depth(comps[0]), depth(comps[1]))
        memo[aspect] = value
        return value

    for name in ASPECT_TABLE:
        depth(name)
    return memo


# Crafting depth of each aspect (0 = primal), used to list the simplest
# aspects first in the UI.
COMPLEXITY: Dict[str, int] = _build_complexity()
