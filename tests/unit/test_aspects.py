"""Structural invariants of the aspect combination table itself -- these
would catch a typo or a copy/paste mistake in ASPECT_TABLE/PACKS/FLAVOR
long before it ever showed up as a confusing solver or connection-finder
bug."""

from pathlib import Path

from tcsolver import aspects

ICONS_DIR = Path(__file__).resolve().parents[2] / "tcsolver" / "static" / "icons"


def test_components_are_zero_or_two():
    for name, comps in aspects.ASPECT_TABLE.items():
        assert len(comps) in (0, 2), f"{name} has {len(comps)} components"


def test_components_reference_known_aspects():
    for name, comps in aspects.ASPECT_TABLE.items():
        for comp in comps:
            assert comp in aspects.ASPECT_TABLE, f"{name} references unknown aspect {comp!r}"


def test_can_connect_is_symmetric():
    for a in aspects.ASPECT_TABLE:
        for b in aspects.ADJACENCY[a]:
            assert aspects.can_connect(a, b)
            assert aspects.can_connect(b, a), f"{a}->{b} connects but not {b}->{a}"


def test_can_connect_matches_components():
    # can_connect(a, b) should be true exactly when b is one of a's own
    # components, or a is one of b's.
    for a, comps in aspects.ASPECT_TABLE.items():
        for comp in comps:
            assert aspects.can_connect(a, comp)
            assert aspects.can_connect(comp, a)


def test_no_aspect_connects_to_itself():
    for name in aspects.ASPECT_TABLE:
        assert name not in aspects.ADJACENCY[name], f"{name} is listed as its own neighbor"


def test_primal_aspects_have_complexity_zero():
    for name, comps in aspects.ASPECT_TABLE.items():
        if not comps:
            assert aspects.COMPLEXITY[name] == 0


def test_complexity_is_one_plus_harder_component():
    for name, comps in aspects.ASPECT_TABLE.items():
        if comps:
            expected = 1 + max(aspects.COMPLEXITY[c] for c in comps)
            assert aspects.COMPLEXITY[name] == expected


def test_all_aspects_matches_the_table():
    assert aspects.ALL_ASPECTS == frozenset(aspects.ASPECT_TABLE)


def test_flavor_covers_every_aspect():
    assert set(aspects.FLAVOR) == aspects.ALL_ASPECTS


def test_packs_cover_every_aspect_exactly_once():
    seen = []
    for pack_aspects in aspects.PACKS.values():
        seen.extend(pack_aspects)
    assert set(seen) == aspects.ALL_ASPECTS
    assert len(seen) == len(set(seen)), "some aspect is listed in more than one pack"


def test_enabled_aspects_is_the_union_of_the_given_packs():
    enabled = aspects.enabled_aspects(["gregtech", "magic_bees"])
    assert enabled == set(aspects.PACKS["gregtech"]) | set(aspects.PACKS["magic_bees"])


def test_enabled_aspects_ignores_unknown_pack_names():
    assert aspects.enabled_aspects(["not_a_real_pack"]) == set()


def test_default_packs_are_a_valid_pack_name():
    for pack in aspects.DEFAULT_PACKS:
        assert pack in aspects.PACKS


def test_thaumic_tinkerer_aspects_are_present():
    # Regression test: these 7 aspects were missing from the initial port
    # (see aspects.py's module docstring) and were added from the "TC
    # (Aspects)" tab of a GTNH guide spreadsheet.
    expected = {
        "aequalitas": ["cognitio", "ordo"],
        "primordium": ["motus", "vacuos"],
        "astrum": ["lux", "primordium"],
        "caelum": ["vitreus", "metallum"],
        "gloria": ["humanus", "iter"],
        "tabernus": ["tutamen", "iter"],
        "vesania": ["cognitio", "vitium"],
    }
    for name, comps in expected.items():
        assert aspects.ASPECT_TABLE[name] == comps
    assert set(aspects.PACKS["thaumic_tinkerer"]) == set(expected)


def test_every_aspect_has_an_icon_file():
    # Every page renders <img src="/static/icons/{aspect}.svg"> for any
    # enabled aspect -- a new aspect with no icon file silently shows a
    # broken image everywhere instead of failing anything.
    missing = [name for name in aspects.ALL_ASPECTS if not (ICONS_DIR / f"{name}.svg").is_file()]
    assert not missing, f"no icon file for: {missing}"


def test_default_packs_is_the_gtnh_preset():
    # Every page must open with the same GTNH preset pre-checked (see
    # packs.js's GTNH_PRESET) -- not just vanilla_tc.
    assert set(aspects.DEFAULT_PACKS) == {
        "vanilla_tc", "gregtech", "forbidden_magic", "magic_bees", "thaumic_tinkerer",
    }
