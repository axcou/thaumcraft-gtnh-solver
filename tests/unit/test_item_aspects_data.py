"""Structural invariants of the Item Aspect Lookup page's static dataset
(tcsolver/static/data/item_aspects.json, generated from the "GTNH Aspects"
community spreadsheet) -- catches a bad regeneration before it reaches the
page's search/filter logic."""

import json
from pathlib import Path

from tcsolver import aspects

DATA_PATH = Path(__file__).resolve().parents[2] / "tcsolver" / "static" / "data" / "item_aspects.json"


def _load():
    with DATA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def test_file_exists_and_parses():
    data = _load()
    assert set(data) == {"aspects", "items"}


def test_every_declared_aspect_is_a_known_aspect():
    data = _load()
    for aspect in data["aspects"]:
        assert aspect in aspects.ALL_ASPECTS, f"unknown aspect {aspect!r}"


def test_every_item_has_a_name_and_at_least_one_aspect():
    data = _load()
    for item in data["items"]:
        assert set(item) == {"name", "aspects"}
        assert item["name"].strip()
        assert item["aspects"], f"{item['name']} has no aspects"


def test_every_item_aspect_key_is_declared_and_amount_is_positive():
    data = _load()
    declared = set(data["aspects"])
    for item in data["items"]:
        for aspect, amount in item["aspects"].items():
            assert aspect in declared, f"{item['name']}: undeclared aspect {aspect!r}"
            assert amount > 0, f"{item['name']}: non-positive amount for {aspect!r}"


def test_dataset_is_reasonably_large():
    # A regression guard against a truncated/empty regeneration.
    data = _load()
    assert len(data["items"]) > 10_000


def test_no_duplicate_name_and_aspects_entries():
    # Regression test: the raw "GTNH Aspects" sheet had 778 groups of
    # exact (name, aspects) duplicate rows (2039 redundant rows total),
    # which showed up as literal duplicate rows on the Item Aspect Lookup
    # page -- most visibly among the purest (single-aspect) items, which
    # sort to the top whenever a specific aspect is filtered.
    data = _load()
    seen = set()
    duplicates = []
    for item in data["items"]:
        key = (item["name"], tuple(sorted(item["aspects"].items())))
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    assert not duplicates, f"{len(duplicates)} duplicate (name, aspects) rows, e.g. {duplicates[:5]}"
