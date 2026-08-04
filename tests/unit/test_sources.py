"""Structural invariants of ASPECT_SOURCES -- catches a typo or a bad
port from the source spreadsheet before it reaches the Aspect Sources
page's filters."""

from tcsolver import aspects
from tcsolver.sources import ASPECT_SOURCES


def test_every_key_is_a_known_aspect():
    for name in ASPECT_SOURCES:
        assert name in aspects.ALL_ASPECTS, f"{name!r} is not a known aspect"


def test_every_aspect_has_at_least_one_source():
    for name, entries in ASPECT_SOURCES.items():
        assert entries, f"{name} has an empty source list"


def test_impurity_is_a_small_non_negative_int():
    for name, entries in ASPECT_SOURCES.items():
        for entry in entries:
            assert isinstance(entry["impurity"], int)
            assert 0 <= entry["impurity"] <= 4, f"{name}: {entry!r}"


def test_highlight_is_good_hard_or_none():
    for name, entries in ASPECT_SOURCES.items():
        for entry in entries:
            assert entry["highlight"] in (None, "good", "hard"), f"{name}: {entry!r}"


def test_item_text_is_non_empty():
    for name, entries in ASPECT_SOURCES.items():
        for entry in entries:
            assert entry["item"].strip(), f"{name} has a blank item name"
