"""Metallurgic Perfection ("nugget dupe") infusion recipes.

How many of which aspects each metal's 2x nugget must absorb, originally
ported from the "Metallurgic Perfection Recipes" tab of a community
spreadsheet:
https://docs.google.com/spreadsheets/d/1Llvu91Vmn4RcCE__lKV8p_MIR9tiaV2URGbkombvlkE

32 of the entries were overridden with the user's own verified values
from a personal spreadsheet:
https://docs.google.com/spreadsheets/d/10YTJdpHYbJ2p7iFn0OiTCVWCQS8XPZUpC6CCBD-Ovls
("Steel" is new -- it wasn't in the original port at all).

The sheet spells one aspect "Nebrisium" -- normalized here to this
project's own id for it, "nebrisum" (see aspects.FLAVOR["nebrisum"] =
"cheatiness").
"""

from __future__ import annotations

from typing import Dict, List, TypedDict


class AspectRequirement(TypedDict):
    aspect: str
    amount: int


class MetalRecipe(TypedDict):
    metal: str
    requires: List[AspectRequirement]


METALLURGIC_RECIPES: List[MetalRecipe] = [
    {"metal": "Adamantium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Alduorite", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Altarus", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Aluminum", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "volatus", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Angmallen", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Antimony", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "aqua", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Ardite", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Arsenic", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "venenum", "amount": 3}]},
    {"metal": "Barium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "vinculum", "amount": 3}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Bedrockium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Beryllium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "lucrum", "amount": 1}]},
    {"metal": "Bismuth", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "instrumentum", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Caesium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}]},
    {"metal": "Callisto Ice", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Carmot", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Celenegil", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Cerium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Ceruclase", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Chrome", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "magneto", "amount": 1}]},
    {"metal": "Chrysotile", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "aer", "amount": 1}, {"aspect": "aqua", "amount": 1}, {"aspect": "sano", "amount": 1}, {"aspect": "tenebrae", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Cobalt", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "instrumentum", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Copper", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Dark Iron", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Duralumin", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "permutatio", "amount": 2}, {"aspect": "sano", "amount": 1}, {"aspect": "volatus", "amount": 1}]},
    {"metal": "Dysprosium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Erbium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Eximite", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Force", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "potentia", "amount": 5}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Gadolinium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Gallium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "electrum", "amount": 1}]},
    {"metal": "Gold", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "lucrum", "amount": 1}]},
    {"metal": "Haederoth", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Hepatizon", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Holmium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Infuscolium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Inolashite", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Iron", "requires": [{"aspect": "metallum", "amount": 2}]},
    {"metal": "Lanthanum", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Lead", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Ledox", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Lithium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "potentia", "amount": 2}, {"aspect": "vitreus", "amount": 1}]},
    {"metal": "Magnesium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "sano", "amount": 1}]},
    {"metal": "Manganese", "requires": [{"aspect": "metallum", "amount": 5}]},
    {"metal": "Manyullyn", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "strontio", "amount": 2}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Meteoric Iron", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "magneto", "amount": 1}]},
    {"metal": "Mithril", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Molybdenum", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "instrumentum", "amount": 1}]},
    {"metal": "Mytryl", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Neodymium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "magneto", "amount": 2}]},
    {"metal": "Nickel", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "ignis", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Orichalcum", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Oureclase", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Pig Iron", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Praseodymium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Prometheum", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Promethium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Realgar", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Rubidium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "vitreus", "amount": 1}]},
    {"metal": "Rubracium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Sanguinite", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Scandium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}]},
    {"metal": "Shadow Iron", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Silicon", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "tenebrae", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Silver", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "lucrum", "amount": 1}]},
    {"metal": "Steel", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Strontium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "strontio", "amount": 1}]},
    {"metal": "Tantalum", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "vinculum", "amount": 1}]},
    {"metal": "Tartarite", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Tellurium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Terbium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Thulium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Tin", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "vitreus", "amount": 1}]},
    {"metal": "Vanadium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}]},
    {"metal": "Vinteum", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "vitreus", "amount": 2}, {"aspect": "praecantatio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Vulcanite", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Vyroxeres", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "nebrisum", "amount": 2}, {"aspect": "ordo", "amount": 1}]},
    {"metal": "Ytterbium", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "radio", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
    {"metal": "Zinc", "requires": [{"aspect": "metallum", "amount": 2}, {"aspect": "sano", "amount": 1}, {"aspect": "permutatio", "amount": 1}]},
]
