"""Community-curated cheap/pure item sources for each aspect.

Ported verbatim from the "EasyPure Aspect Sources" sheet:
https://docs.google.com/spreadsheets/d/1Llvu91Vmn4RcCE__lKV8p_MIR9tiaV2URGbkombvlkE

Each entry is a scannable item, how many "impurities" (unwanted extra
aspects picked up alongside the one you want) it carries, and an optional
highlight matching the sheet's own color coding:
- "good": green in the sheet -- an especially good/surprising find.
- "hard": red in the sheet -- a pure (0-impurity) source, but a difficult
  one to get your hands on.

Not every aspect in ASPECT_TABLE has an entry here -- the sheet doesn't
cover the newer GT:NH-specific ones (coralos, dreadia, tincturem, sanctus,
exubitor, saxum, granum, mru, radiation, matrix).
"""

from __future__ import annotations

from typing import Dict, List, Optional, TypedDict


class SourceItem(TypedDict):
    item: str
    impurity: int
    highlight: Optional[str]


ASPECT_SOURCES: Dict[str, List[SourceItem]] = {
    "aer": [
        {"item": "Sliver of Air (1)", "impurity": 0, "highlight": None},
        {"item": "[IC2] Rubber Sheet (5)", "impurity": 0, "highlight": "good"},
        {"item": "Feather (1:2 Volatus)", "impurity": 1, "highlight": None},
        {"item": "Rose Bush (1:1 Herba)", "impurity": 1, "highlight": None},
        {"item": "Aer Fragment (6:1 Herba)", "impurity": 1, "highlight": "good"},
        {"item": "Sugar Cane (1:1 Herba, 1:1 Aqua)", "impurity": 2, "highlight": None},
    ],
    "alienis": [
        {"item": "Ender Pearl (4:4 Iter, 4:2 Praecantatio)", "impurity": 2, "highlight": None},
        {"item": "Moon Turf (1:1 Tenebrae, 1:1 Vacuos)", "impurity": 2, "highlight": None},
    ],
    "aqua": [
        {"item": "Fresh Water (1)", "impurity": 0, "highlight": None},
        {"item": "Water Bottle (1:1 Vitreus)", "impurity": 1, "highlight": None},
        {"item": "Clay (1:1 Terra)", "impurity": 1, "highlight": None},
    ],
    "arbor": [
        {"item": "Wood (4)", "impurity": 0, "highlight": None},
        {"item": "Stick (1)", "impurity": 0, "highlight": None},
        {"item": "Framing Board (1)", "impurity": 0, "highlight": None},
    ],
    "auram": [
        {"item": "Terrawart (8:4 Praecantatio, 8:4 Victus)", "impurity": 2, "highlight": None},
    ],
    "bestia": [
        {"item": "String (1:1 Pannus)", "impurity": 1, "highlight": None},
        {"item": "Spider Eye (2:2 Sensus, 2:2 Venenum)", "impurity": 2, "highlight": None},
    ],
    "cognitio": [
        {"item": "Knowledge Fragment (8)", "impurity": 0, "highlight": "hard"},
        {"item": "Printed Pages (2)", "impurity": 0, "highlight": None},
        {"item": "Cardboard (1:1 Fabrico)", "impurity": 1, "highlight": None},
        {"item": "Book (1:1 Pannus)", "impurity": 1, "highlight": None},
        {"item": "Chad (1:1 Perditio)", "impurity": 1, "highlight": "good"},
        {"item": "Paper (4:2 Aqua, 4:1 Arbor)", "impurity": 2, "highlight": None},
        {"item": "Zombie Brain (4:2 Corpus, 4:2 Exanimis)", "impurity": 2, "highlight": None},
    ],
    "corpus": [
        {"item": "Stock (1)", "impurity": 0, "highlight": None},
        {"item": "Rotten Flesh (2:1 Humanus)", "impurity": 1, "highlight": None},
        {"item": "Sausage (3:1 Victus)", "impurity": 1, "highlight": None},
        {"item": "Wool of Bat (1:1 Volatus)", "impurity": 1, "highlight": None},
        {"item": "Raw Fish (3:1 Aqua, 3:1 Victus)", "impurity": 2, "highlight": None},
    ],
    "desidia": [
        {"item": "Bed (4:6 Pannus, 4:3 Fabrico)", "impurity": 2, "highlight": None},
        {"item": "Sloth Shard (2:1 Infernus, 2:1 Vitreus)", "impurity": 2, "highlight": None},
    ],
    "electrum": [
        {"item": "Most Fine Wire (1)", "impurity": 0, "highlight": None},
    ],
    "exanimis": [
        {"item": "Skeleton Skull (4:4 Spiritus, 4:4 Mortuus)", "impurity": 2, "highlight": None},
        {"item": "Small Bone Segment (3:2 Mortuus, 3:1 Corpus)", "impurity": 2, "highlight": None},
        {"item": "Medium Bone Segment (6:4 Mortuus, 6:2 Corpus)", "impurity": 2, "highlight": None},
        {"item": "Large Bone Segment (9:6 Mortuus, 9:3 Corpus)", "impurity": 2, "highlight": None},
    ],
    "fabrico": [
        {"item": "Crafting Table (4)", "impurity": 0, "highlight": None},
        {"item": "Copper Foil (1)", "impurity": 0, "highlight": None},
    ],
    "fames": [
        {"item": "Sugar (1)", "impurity": 0, "highlight": None},
        {"item": "Melon (1)", "impurity": 0, "highlight": None},
    ],
    "gelum": [
        {"item": "Snowball (1)", "impurity": 0, "highlight": None},
    ],
    "gula": [
        {"item": "Gluttony Shard (2:1 Infernus, 2:1 Vitreus)", "impurity": 2, "highlight": None},
    ],
    "herba": [
        {"item": "Mud Ball (4)", "impurity": 0, "highlight": None},
        {"item": "Weed (1)", "impurity": 0, "highlight": None},
        {"item": "Leaves (1)", "impurity": 0, "highlight": None},
        {"item": "Vanilla Saplings (2:1 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Edible Salt (9:4 Metallum)", "impurity": 1, "highlight": None},
    ],
    "humanus": [
        {"item": "Rotten Flesh (1:2 Corpus)", "impurity": 1, "highlight": None},
    ],
    "ignis": [
        {"item": "Nether Cobblestone Slab (1)", "impurity": 0, "highlight": None},
        {"item": "Gunpowder (4:4 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Wood Ash (1:1 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Charcoal (2:2 Potentia)", "impurity": 1, "highlight": None},
        {"item": "Sulfur Dust (1:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Nether Brick (1:1 Infernus)", "impurity": 1, "highlight": None},
        {"item": "Ignis Fragment (6:1 Herba)", "impurity": 1, "highlight": None},
        {"item": "Carbon Dust (1:1 Vitreus, 1:1 Perditio)", "impurity": 2, "highlight": None},
        {"item": "Chili Pepper (1:1 Messis, 1:1 Fames)", "impurity": 2, "highlight": None},
        {"item": "Fertilizer (3:2 Sano, 3:1 Herba)", "impurity": 2, "highlight": None},
        {"item": "Silicon Plate (1:1 Ordo, 1:1 Sensus)", "impurity": 2, "highlight": None},
    ],
    "infernus": [
        {"item": "Nether Brick (1:1 Ignis)", "impurity": 1, "highlight": None},
        {"item": "Netherrack (1:2 Terra, 1:1 Ignis)", "impurity": 2, "highlight": None},
        {"item": "Nether Wart (1:1 Herba, 1:1 Praecantatio)", "impurity": 2, "highlight": None},
    ],
    "instrumentum": [
        {"item": "Long Stone Rod (1)", "impurity": 0, "highlight": "good"},
        {"item": "Rubber Round (1)", "impurity": 0, "highlight": None},
        {"item": "Flint (1:1 Terra)", "impurity": 1, "highlight": None},
        {"item": "Wooden Spade (1:2 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Stone Spade (2:1 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Soy Milk (1:1 Fabrico, 1:1 Ordo)", "impurity": 2, "highlight": None},
        {"item": "Most Screws (3:1 Fabrico, 3:1 Ordo)", "impurity": 2, "highlight": None},
    ],
    "invidia": [
        {"item": "Redstone Comparator (2:2 Machina, 2:2 Ordo)", "impurity": 2, "highlight": None},
        {"item": "Eye of Ender (4:4 Sensus, 4:4 Alienis, 4:3 Praecantatio)", "impurity": 3, "highlight": None},
    ],
    "ira": [
        {"item": "Fusewood (2:3 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Wrath Shard (2:1 Infernus, 2:1 Vitreus)", "impurity": 2, "highlight": None},
        {"item": "Moon Dungeon Brick (1:4 Alienis, 1:1 Superbia)", "impurity": 2, "highlight": None},
        {"item": "Fire Charge (1:2 Ignis, 1:1 Perditio)", "impurity": 2, "highlight": None},
    ],
    "iter": [
        {"item": "Empty Crate (2:1 Vacuos)", "impurity": 1, "highlight": "good"},
        {"item": "Empty Plastic Fuel Can (1:1 Vacuos)", "impurity": 1, "highlight": None},
        {"item": "Fence Gate (1:4 Arbor, 1:1 Machina)", "impurity": 2, "highlight": None},
        {"item": "Boat (4:4 Aqua, 4:3 Arbor)", "impurity": 2, "highlight": None},
        {"item": "Ender Pearl (4:4 Alienis, 4:2 Praecantatio)", "impurity": 2, "highlight": None},
        {"item": "GT Plunger (2:2 Instrumentum, 2:2 Vacuos)", "impurity": 2, "highlight": None},
    ],
    "limus": [
        {"item": "Slime Ball (2)", "impurity": 0, "highlight": None},
        {"item": "Firm Tofu (3:1 Instrumentum)", "impurity": 1, "highlight": None},
        {"item": "Egg (1:1 Victus, 1:1 Aqua)", "impurity": 2, "highlight": None},
    ],
    "lucrum": [
        {"item": "Gold Coin (1)", "impurity": 0, "highlight": None},
        {"item": "Industrial Silver Credit (1)", "impurity": 0, "highlight": None},
        {"item": "Etched Sandy Stone (2:6 Terra)", "impurity": 1, "highlight": "good"},
        {"item": "Emerald (5:4 Vitreus)", "impurity": 1, "highlight": None},
        {"item": "Greed Shard (2:1 Infernus, 2:1 Vitreus)", "impurity": 2, "highlight": None},
        {"item": "Gold Ingot (2:2 Metallum, 2:1 Permutatio)", "impurity": 2, "highlight": None},
    ],
    "lux": [
        {"item": "Torch (1)", "impurity": 0, "highlight": None},
        {"item": "Glowing Coral (1)", "impurity": 0, "highlight": None},
        {"item": "Glowstone Dust (2:1 Sensus)", "impurity": 1, "highlight": None},
        {"item": "Glowstone Block (10:3 Sensus)", "impurity": 1, "highlight": None},
        {"item": "Quarried Brick (4:4 Terra)", "impurity": 1, "highlight": None},
        {"item": "Quarried Block (4:2 Terra, 4:2 Ordo)", "impurity": 2, "highlight": None},
    ],
    "luxuria": [
        {"item": "Lust Shard (2:1 Infernus, 2:1 Vitreus)", "impurity": 2, "highlight": None},
        {"item": "[Minecraft] Lead (2:2 Bestia, 2:2 Pannus, 2:1 Limus)", "impurity": 3, "highlight": None},
    ],
    "machina": [
        {"item": "Wood Button (1)", "impurity": 0, "highlight": None},
        {"item": "Redstone Torch (1:1 Potentia)", "impurity": 1, "highlight": None},
        {"item": "Redstone (1:2 Potentia)", "impurity": 1, "highlight": None},
        {"item": "Stone Button (1:1 Terra)", "impurity": 1, "highlight": None},
        {"item": "Small Stone Gear (1:1 Motus, 1:1 Terra)", "impurity": 2, "highlight": None},
        {"item": "[Wooden] Fence Gate (1:4 Arbor, 1:1 Iter)", "impurity": 2, "highlight": None},
    ],
    "magneto": [
        {"item": "Magnetic Neodymium Rod (1)", "impurity": 0, "highlight": None},
        {"item": "Magnetic Iron Ingot (1:3 Metallum)", "impurity": 1, "highlight": None},
    ],
    "messis": [
        {"item": "Gravy (1)", "impurity": 0, "highlight": None},
        {"item": "Batter (1)", "impurity": 0, "highlight": None},
        {"item": "Gregtech Flour (2:1 Perditio)", "impurity": 1, "highlight": None},
    ],
    "metallum": [
        {"item": "Iron/Tin/Copper Oreberry (1)", "impurity": 0, "highlight": None},
        {"item": "Iron Nugget (1)", "impurity": 0, "highlight": None},
        {"item": "Heavy Cream (1)", "impurity": 0, "highlight": None},
        {"item": "Iron Ingot (4:1 Permutatio)", "impurity": 1, "highlight": None},
        {"item": "Edible Salt (4:9 Herba)", "impurity": 1, "highlight": "good"},
        {"item": "Wooden Spike (14:18 Telum, 14:4 Arbor)", "impurity": 2, "highlight": None},
        {"item": "Printed Silicon (27:1 Ignis, 27:1 Sensus, 27:1 Ordo)", "impurity": 3, "highlight": None},
    ],
    "meto": [
        {"item": "Wooden Hoe (1)", "impurity": 0, "highlight": None},
        {"item": "Cobblestone Slab (1:1 Arbor, 1:1 Instrumentum)", "impurity": 2, "highlight": None},
    ],
    "mortuus": [
        {"item": "Bone (2:1 Corpus)", "impurity": 1, "highlight": None},
        {"item": "Dead Wood (2:4 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Potion of Harming (6:4 Praecantatio, 6:1 Aqua)", "impurity": 2, "highlight": None},
        {"item": "Raw Venison (3:2 Victus, 3:1 Bestia)", "impurity": 2, "highlight": None},
        {"item": "Belladonna (4:4 Venenum, 4:2 Herba)", "impurity": 2, "highlight": None},
    ],
    "motus": [
        {"item": "Long Polyethylene Rod (2)", "impurity": 0, "highlight": None},
        {"item": "Tiny Plastic Fluid Pipe (1)", "impurity": 0, "highlight": None},
        {"item": "Cookie Jar (1)", "impurity": 0, "highlight": None},
        {"item": "Polyethylene Pulp (2:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Raw Rubber Dust (2:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Rubber Sheet (2:1 Fabrico)", "impurity": 1, "highlight": None},
    ],
    "nebrisum": [
        {"item": "Platinum Ingot (1:3 Metallum)", "impurity": 1, "highlight": None},
        {"item": "Platinum Metallic Powder Dust (1:2 Metallum, 1:1 Terra)", "impurity": 2, "highlight": None},
        {"item": "Platinum Dust (1:2 Metallum, 1:1 Perditio)", "impurity": 2, "highlight": None},
    ],
    "ordo": [
        {"item": "Forestry Beeswax (3)", "impurity": 0, "highlight": "good"},
        {"item": "Sliver of Order (1)", "impurity": 0, "highlight": None},
        {"item": "Candleberry (1:2 Messis)", "impurity": 1, "highlight": None},
        {"item": "Chiselled Stone Bricks (1:1 Terra)", "impurity": 1, "highlight": "good"},
        {"item": "Soy Milk (1:1 Instrumentum, 1:1 Fabrico)", "impurity": 2, "highlight": None},
        {"item": "Order Shard (2:1 Vitreus, 2:1 Praecantatio)", "impurity": 2, "highlight": None},
        {"item": "Silicon Plate (1:1 Ignis, 1:1 Sensus)", "impurity": 2, "highlight": None},
        {"item": "Silverwood Log (1:3 Arbor, 1:1 Praecantatio)", "impurity": 2, "highlight": None},
    ],
    "pannus": [
        {"item": "Cotton (1)", "impurity": 0, "highlight": None},
        {"item": "Carpet (2)", "impurity": 0, "highlight": None},
        {"item": "Wool (4:1 Fabrico)", "impurity": 1, "highlight": None},
    ],
    "perditio": [
        {"item": "Tiny Pile of Netherrack Dust (1)", "impurity": 0, "highlight": None},
        {"item": "Tiny Pile of Ashes (1)", "impurity": 0, "highlight": None},
        {"item": "Mince Meat (1)", "impurity": 0, "highlight": None},
        {"item": "Cobblestone (1:1 Terra)", "impurity": 1, "highlight": None},
    ],
    "perfodio": [
        {"item": "Wooden Pickaxe (1:3 Arbor)", "impurity": 1, "highlight": None},
        {"item": "GT Pickaxe (4:2 Instrumentum)", "impurity": 1, "highlight": None},
        {"item": "Marble Dust (1:1 Perditio)", "impurity": 1, "highlight": None},
    ],
    "permutatio": [
        {"item": "Honey Drop (2:2 Victus)", "impurity": 1, "highlight": "good"},
        {"item": "Copper Ingot (2:3 Metallum)", "impurity": 1, "highlight": None},
        {"item": "Natura Pile of Ashes (1:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Natura Barley Seeds (1:1 Herba)", "impurity": 1, "highlight": None},
        {"item": "Soybean (1:1 Messis, 1:1 Fames)", "impurity": 2, "highlight": None},
        {"item": "Quicksilver (2:3 Metallum, 2:1 Venenum)", "impurity": 2, "highlight": None},
        {"item": "Rainbow Cacti (4:3 Herba, 4:2 Sensus, 4:1 Aqua, 4:1 Perditio)", "impurity": 4, "highlight": None},
    ],
    "potentia": [
        {"item": "Redstone Conduit (1)", "impurity": 0, "highlight": None},
        {"item": "Redstone (2:1 Machina)", "impurity": 1, "highlight": None},
        {"item": "Charcoal/Coal (2:2 Ignis)", "impurity": 1, "highlight": None},
        {"item": "Quartz Sand (1:1 Vitreus, 1:1 Perditio)", "impurity": 2, "highlight": None},
        {"item": "Bloodwood (2:2 Arbor, 2:1 Metallum)", "impurity": 2, "highlight": None},
    ],
    "praecantatio": [
        {"item": "Greatwood Log (1:3 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Magic Wax (2:1 Ordo)", "impurity": 1, "highlight": None},
        {"item": "Magic Wood (2:4 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Magic Leaves (1:1 Herba)", "impurity": 1, "highlight": None},
        {"item": "Magic Wood Planks (1:1 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Nether Wart (1:1 Herba, 1:1 Infernus)", "impurity": 2, "highlight": None},
        {"item": "Mossy Cobblestone (1:1 Herba, 1:1 Terra)", "impurity": 2, "highlight": None},
        {"item": "Ender Pearl (2:4 Alienis, 2:4 Iter)", "impurity": 2, "highlight": None},
        {"item": "Terra Wart (4:8 Auram, 4:4 Victus)", "impurity": 2, "highlight": None},
        {"item": "Blaze Powder (4:6 Ignis, 4:2 Instrumentum)", "impurity": 2, "highlight": None},
        {"item": "Chiselled Sandstone (1:3 Perditio, 1:2 Terra)", "impurity": 2, "highlight": "good"},
        {"item": "Magic Sapling (2:1 Herba, 2:1 Arbor)", "impurity": 2, "highlight": None},
    ],
    "radio": [
        {"item": "Vanadium Dust (1:2 Metallum, 1:1 Perditio)", "impurity": 2, "highlight": None},
    ],
    "sano": [
        {"item": "Fresh Milk (1)", "impurity": 0, "highlight": None},
        {"item": "Milk Powder (2:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Fertilizer (2:3 Ignis, 2:1 Herba)", "impurity": 2, "highlight": None},
        {"item": "Calcium Dust (1:1 Perditio, 1:1 Tutamen)", "impurity": 2, "highlight": None},
        {"item": "Magnesium Dust (1:2 Metallum, 1:1 Perditio)", "impurity": 2, "highlight": None},
        {"item": "Zinc Dust (1:2 Metallum, 1:1 Perditio)", "impurity": 2, "highlight": None},
    ],
    "sensus": [
        {"item": "Lapis/Sodalite/Lazurite Dust (1)", "impurity": 0, "highlight": None},
        {"item": "Bone Meal (1)", "impurity": 0, "highlight": None},
        {"item": "All Dyes (1)", "impurity": 0, "highlight": None},
    ],
    "spiritus": [
        {"item": "Ghostwood Log (1:3 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Ghostwood Sapling (1:2 Herba, 1:2 Arbor)", "impurity": 2, "highlight": None},
        {"item": "Soul Sand (1:1 Vinculum, 1:1 Terra)", "impurity": 2, "highlight": None},
    ],
    "strontio": [
        {"item": "Scrap Boxes (4)", "impurity": 0, "highlight": None},
        {"item": "Alumite Dust (2:1 Perditio)", "impurity": 1, "highlight": None},
    ],
    "superbia": [
        {"item": "Moon Dungeon Brick (1:4 Alienis, 1:1 Ira)", "impurity": 2, "highlight": None},
        {"item": "Pride Shard (2:1 Infernus, 2:1 Vitreus)", "impurity": 2, "highlight": None},
        {"item": "Golden Helmet (2:11 Metallum, 2:7 Lucrum, 2:2 Tutamen)", "impurity": 3, "highlight": None},
    ],
    "telum": [
        {"item": "Empty Glass Arrow Head (1:1 Vacuous)", "impurity": 1, "highlight": "good"},
        {"item": "[Witchery] Quicklime (1:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Wooden Spike (18:14 Metallum, 18:4 Arbor)", "impurity": 2, "highlight": None},
    ],
    "tempestas": [
        {"item": "Iron Fence (1:2 Metallum, 1:1 Potentia)", "impurity": 2, "highlight": None},
        {"item": "Ash Cloud (1:1 Aer, 1:1 Ignis, 1:1 Volatus)", "impurity": 3, "highlight": None},
    ],
    "tempus": [
        {"item": "Watch (4:2 Machina, 4:1 Potentia)", "impurity": 2, "highlight": None},
    ],
    "tenebrae": [
        {"item": "Abyssal Block Slab (1)", "impurity": 0, "highlight": "good"},
        {"item": "Basalt Dust (1:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "End Stone (1:1 Terra)", "impurity": 1, "highlight": None},
        {"item": "Darkwood (2:3 Arbor)", "impurity": 1, "highlight": None},
        {"item": "Raven's Feather (1:1 Aer, 1:2 Volatus)", "impurity": 2, "highlight": None},
        {"item": "Silicon Dust (1:1 Perditio, 1:2 Metallum)", "impurity": 2, "highlight": None},
        {"item": "White Mushroom (1:1 Fames, 1:1 Messis)", "impurity": 2, "highlight": None},
        {"item": "Moon Turf (1:1 Alienis, 1:1 Vacuos)", "impurity": 2, "highlight": None},
        {"item": "Obsidian (1:2 Ignis, 1:2 Terra)", "impurity": 2, "highlight": None},
    ],
    "terminus": [
        {"item": "Infinity Catalyst (5:12 Permutatio)", "impurity": 1, "highlight": None},
        {"item": "Crystal Matrix Ingot (1:32 Vitreus, 1:8 Potentia)", "impurity": 2, "highlight": None},
    ],
    "terra": [
        {"item": "Dirt (2)", "impurity": 0, "highlight": None},
        {"item": "Gravel (2)", "impurity": 0, "highlight": None},
        {"item": "Hardened Clay (4:1 Ignis)", "impurity": 1, "highlight": None},
        {"item": "Clay (1:1 Aqua)", "impurity": 1, "highlight": None},
    ],
    "tutamen": [
        {"item": "Static Boots (3)", "impurity": 0, "highlight": None},
        {"item": "Apiarist's Armors (1-3)", "impurity": 0, "highlight": None},
        {"item": "Black Granite Dust (1:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Red Granite Dust (1:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Calcium Dust (1:1 Sano, 1:1 Perditio)", "impurity": 2, "highlight": None},
        {"item": "Leather (1:2 Pannus, 1:1 Bestia)", "impurity": 2, "highlight": None},
        {"item": "Wooden Leggings (2:21 Arbor, 2:3 Limus, 2:1 Instrumentum)", "impurity": 3, "highlight": None},
    ],
    "vacuos": [
        {"item": "Glass Bottle (1)", "impurity": 0, "highlight": None},
        {"item": "Bowl (1)", "impurity": 0, "highlight": None},
        {"item": "Chest (4:6 Arbor)", "impurity": 1, "highlight": None},
    ],
    "venenum": [
        {"item": "Poison Glass Arrow Head (1:1 Telum)", "impurity": 1, "highlight": None},
        {"item": "Arsenic Dust (3:1 Perditio)", "impurity": 1, "highlight": None},
        {"item": "Belladonna (4:4 Mortuus, 4:2 Herba)", "impurity": 1, "highlight": None},
        {"item": "Spider Eye (2:2 Bestia, 2:2 Sensus)", "impurity": 2, "highlight": None},
        {"item": "Quicksilver (1:3 Metallum, 1:2 Permutatio)", "impurity": 2, "highlight": None},
    ],
    "victus": [
        {"item": "Honey Drop (2:2 Permutatio)", "impurity": 1, "highlight": None},
        {"item": "Natura Barley (2:2 Messis)", "impurity": 1, "highlight": None},
        {"item": "Sausage (1:3 Corpus)", "impurity": 1, "highlight": None},
        {"item": "All Natura Berries (1:1 Messis)", "impurity": 1, "highlight": None},
        {"item": "Egg (1:1 Limus, 1:1 Bestia)", "impurity": 2, "highlight": None},
        {"item": "Filled Tin Can (4:2 Fabrico, 4:2 Metallum, 4:2 Vitreus)", "impurity": 3, "highlight": None},
    ],
    "vinculum": [
        {"item": "Honey Comb (2)", "impurity": 0, "highlight": None},
        {"item": "Quicksand (4:2 Terra)", "impurity": 1, "highlight": None},
        {"item": "Amber (2:2 Vitreus)", "impurity": 1, "highlight": None},
        {"item": "Dense Web (4:2 Pannus)", "impurity": 1, "highlight": None},
    ],
    "vitium": [
        {"item": "Tainted Goo (3:1 Limus)", "impurity": 1, "highlight": None},
    ],
    "vitreus": [
        {"item": "Glass (1)", "impurity": 0, "highlight": None},
        {"item": "Quite Clear Glass (2)", "impurity": 0, "highlight": None},
        {"item": "Glass Dust (2:1 Perditio)", "impurity": 1, "highlight": None},
    ],
    "volatus": [
        {"item": "Scribing Tools (1)", "impurity": 0, "highlight": "hard"},
        {"item": "Feather (2:1 Aer)", "impurity": 1, "highlight": None},
        {"item": "Wool of Bat (1:1 Corpus)", "impurity": 1, "highlight": "good"},
        {"item": "Aluminum Dust (1:2 Metallum, 1:1 Perditio)", "impurity": 2, "highlight": None},
        {"item": "Skyberry (4:4 Perditio, 4:1 Victus, 4:1 Messis)", "impurity": 3, "highlight": None},
    ],
}
