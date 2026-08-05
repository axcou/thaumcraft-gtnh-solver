"""Structural invariants of METALLURGIC_RECIPES -- catches a typo or a bad
port from the source spreadsheet before it reaches the Metallurgic
Perfection page."""

from tcsolver import aspects
from tcsolver.metallurgy import METALLURGIC_RECIPES


def test_every_metal_has_at_least_one_requirement():
    for recipe in METALLURGIC_RECIPES:
        assert recipe["requires"], f"{recipe['metal']} has no requirements"


def test_every_requirement_references_a_known_aspect():
    for recipe in METALLURGIC_RECIPES:
        for req in recipe["requires"]:
            assert req["aspect"] in aspects.ALL_ASPECTS, (
                f"{recipe['metal']}: unknown aspect {req['aspect']!r}"
            )


def test_every_requirement_amount_is_a_positive_int():
    for recipe in METALLURGIC_RECIPES:
        for req in recipe["requires"]:
            assert isinstance(req["amount"], int)
            assert req["amount"] > 0, f"{recipe['metal']}: {req!r}"


def test_metal_names_are_unique():
    names = [recipe["metal"] for recipe in METALLURGIC_RECIPES]
    assert len(names) == len(set(names))


def test_every_metal_starts_with_metallum():
    # Every recipe infuses a metal nugget, so metallum is always the base
    # requirement -- but not always exactly 2x (e.g. Manganese needs 5x
    # and nothing else, per the user's own verified data).
    for recipe in METALLURGIC_RECIPES:
        first = recipe["requires"][0]
        assert first["aspect"] == "metallum", recipe["metal"]
        assert first["amount"] >= 2, recipe["metal"]
