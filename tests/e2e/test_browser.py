"""End-to-end browser tests (Playwright) for behavior that only exists in
the DOM/CSS/JS and can't be exercised by the pure-Python backend tests:
the Aspect Combination tree diagram and its pan/zoom, the Solver page's
canvas/grid-import-export interactions, the shared pack selector, and the
Connection Helper's result chain.
"""

from __future__ import annotations

import json
import re


def _select_aspect(page, aspect: str) -> None:
    page.wait_for_selector("#combinationList .aspect-card")
    page.click(f'.aspect-card[data-aspect="{aspect}"]')
    page.wait_for_timeout(200)


# --- Aspect Combination: tree diagram ---------------------------------------


def test_tree_matches_expected_node_count(live_server, page):
    # Regression test for the bug where a subtree could silently go
    # missing (wrong node count) instead of rendering.
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "meto")

    node_count = page.eval_on_selector_all("#treeDiagram .tree-box", "els => els.length")
    assert node_count == 47  # tcsolver.aspects.ASPECT_TABLE-derived count for "meto"


def test_tree_boxes_do_not_overlap(live_server, page):
    # Regression test for the float+inline-block width bug that could
    # wrap a sibling subtree onto a new line, overlapping other boxes.
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "meto")

    rects = page.eval_on_selector_all(
        "#treeDiagram .tree-box",
        "els => els.map(el => { const r = el.getBoundingClientRect();"
        " return {x: r.x, y: r.y, w: r.width}; })",
    )
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if abs(a["y"] - b["y"]) >= 5:
                continue
            overlap = a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"]
            assert not overlap, f"boxes overlap on row y={a['y']}: {a} vs {b}"


def test_every_child_box_has_a_connector_reaching_it(live_server, page):
    # Regression test: every child (not just the first) must have a
    # connector line actually touching its top edge -- the old CSS
    # connector (a shared border on a pseudo-element) had a bug where
    # `border: 0 none` deleted the last child's drop-line along with the
    # intentionally-removed outward stub. The new SVG connectors draw
    # each child's drop-line as its own explicit path segment, so this
    # checks that segment lands exactly on each child's box.
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "lux")

    info = page.eval_on_selector(
        "#treeDiagram",
        """el => {
            const diagramRect = el.getBoundingClientRect();
            const boxes = Array.from(el.querySelectorAll('.tree-box')).map(box => {
                const r = box.getBoundingClientRect();
                return {
                    label: box.querySelector('span').textContent,
                    x: r.x + r.width / 2 - diagramRect.x,
                    y: r.y - diagramRect.y,
                };
            });
            const d = el.querySelector('.tree-connectors path').getAttribute('d');
            return {boxes, d};
        }""",
    )
    points = [
        (float(m[0]), float(m[1]))
        for m in re.findall(r"([\d.]+) ([\d.]+)", info["d"])
    ]

    children = [b for b in info["boxes"] if b["label"] != "Lux"]
    assert len(children) == 2
    for child in children:
        assert any(
            abs(px - child["x"]) < 1 and abs(py - child["y"]) < 1 for px, py in points
        ), f"no connector point touches {child['label']}'s box"


def test_tree_centers_parent_over_true_midpoint_of_children(live_server, page):
    # Regression test for the reported bug: a leaf sibling of a much
    # deeper branch used to get dragged far from their shared parent,
    # because the old nested-flexbox layout centered each row on the
    # *combined subtree width* of both children rather than on their own
    # box centers. Tutamen's components are Terra (primal, no further
    # children) and Instrumentum (which branches several levels deep) --
    # exactly the shape that made the bug obvious (Terra ended up ~560px
    # from Tutamen vs. Instrumentum's ~40px).
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "tutamen")

    positions = page.eval_on_selector_all(
        "#treeDiagram .tree-box",
        "els => els.map(el => { const r = el.getBoundingClientRect();"
        " return {label: el.querySelector('span').textContent, x: r.x + r.width / 2}; })",
    )

    def first_x(label):
        return next(p["x"] for p in positions if p["label"] == label)

    parent_x = first_x("Tutamen")
    terra_x = first_x("Terra")
    instrumentum_x = first_x("Instrumentum")

    # the parent must sit exactly at the midpoint of its two children --
    # not off to one side because one child's subtree is much wider
    assert abs(parent_x - (terra_x + instrumentum_x) / 2) < 1
    # both children must be equidistant from their shared parent
    assert abs(abs(parent_x - terra_x) - abs(parent_x - instrumentum_x)) < 1


def test_wheel_zooms_the_tree(live_server, page):
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "lux")

    box = page.locator("#treeWrapper").bounding_box()
    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    page.mouse.move(cx, cy)
    page.mouse.wheel(0, -300)
    page.wait_for_timeout(100)

    transform = page.eval_on_selector("#treeDiagram", "el => el.style.transform")
    scale = float(transform.split("scale(")[1].rstrip(")"))
    assert scale > 1.0


def test_drag_pans_the_tree_by_the_mouse_delta(live_server, page):
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "lux")

    def translate():
        transform = page.eval_on_selector("#treeDiagram", "el => el.style.transform")
        inner = transform.split("translate(")[1].split(")")[0]
        x, y = (float(v.replace("px", "")) for v in inner.split(","))
        return x, y

    before_x, before_y = translate()
    box = page.locator("#treeWrapper").bounding_box()
    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    page.mouse.move(cx, cy)
    page.mouse.down()
    page.mouse.move(cx + 120, cy + 40, steps=5)
    page.mouse.up()
    page.wait_for_timeout(100)
    after_x, after_y = translate()

    assert round(after_x - before_x) == 120
    assert round(after_y - before_y) == 40


def test_selecting_aspect_updates_recipe_and_tree(live_server, page):
    # The root node is always the first one laid out (see layoutTree() in
    # aspect-tree.js), so it's always the first .tree-box in DOM order.
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "lux")
    assert page.eval_on_selector(
        "#treeDiagram", "el => el.querySelector('.tree-box span').textContent"
    ) == "Lux"

    _select_aspect(page, "ignis")
    assert page.eval_on_selector(
        "#treeDiagram", "el => el.querySelector('.tree-box span').textContent"
    ) == "Ignis"


def test_aspect_combination_search_filters_the_list(live_server, page):
    page.goto(f"{live_server}/combinations")
    page.wait_for_selector("#combinationList .aspect-card")
    page.fill("#searchBox", "ignis")
    page.wait_for_timeout(150)
    names = page.eval_on_selector_all(
        "#combinationList .aspect-card .aspect-card-main span",
        "els => els.map(el => el.textContent)",
    )
    assert names == ["Ignis"]


# --- Research Table Solver ---------------------------------------------------


def test_solver_click_bars_and_unbars_a_cell(live_server, page):
    page.goto(f"{live_server}/")
    page.wait_for_selector("#board")
    box = page.locator("#board").bounding_box()
    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2

    def center_pixel():
        return page.evaluate(
            """() => {
                const canvas = document.getElementById('board');
                const ctx = canvas.getContext('2d');
                const d = ctx.getImageData(canvas.width / 2, canvas.height / 2, 1, 1).data;
                return [d[0], d[1], d[2]];
            }"""
        )

    before = center_pixel()
    page.mouse.click(cx, cy)
    page.wait_for_timeout(50)
    barred = center_pixel()
    assert barred == [0, 0, 0]
    assert barred != before

    page.mouse.click(cx, cy)
    page.wait_for_timeout(50)
    assert center_pixel() != barred


def test_export_grid_downloads_a_tcgrid_file(live_server, page):
    page.goto(f"{live_server}/")
    page.wait_for_selector("#board")
    with page.expect_download() as download_info:
        page.click("#exportGridBtn")
    download = download_info.value
    assert download.suggested_filename.endswith(".tcgrid")


def test_import_grid_restores_board_state(live_server, page, tmp_path):
    page.goto(f"{live_server}/")
    page.wait_for_selector("#board")

    grid_file = tmp_path / "sample.tcgrid"
    grid_file.write_text(
        json.dumps(
            {
                "version": 1,
                "radius": 2,
                "packs": ["vanilla_tc"],
                "cells": [
                    {"q": 2, "r": -2, "aspect": "terra", "base": True, "barred": False, "solved": False},
                ],
            }
        )
    )

    page.set_input_files("#importGridInput", str(grid_file))
    page.wait_for_timeout(200)

    assert page.eval_on_selector("#size", "el => el.value") == "3"  # radius 2 -> size 3
    status_text = page.eval_on_selector("#status", "el => el.textContent").lower()
    assert "imported" in status_text


def test_gtnh_preset_checks_the_expected_packs(live_server, page):
    page.goto(f"{live_server}/")
    page.wait_for_selector("#packs button")
    page.click("#packs button")  # the only button in #packs is "GTNH preset"
    checked = page.eval_on_selector_all(
        "#packs input[type=checkbox]",
        "els => els.filter(el => el.checked).map(el => el.value)",
    )
    assert set(checked) == {"vanilla_tc", "gregtech", "forbidden_magic", "magic_bees", "thaumic_tinkerer"}


def test_gtnh_preset_is_checked_by_default_on_load(live_server, page):
    page.goto(f"{live_server}/")
    page.wait_for_selector("#packs input[type=checkbox]")
    checked = page.eval_on_selector_all(
        "#packs input[type=checkbox]",
        "els => els.filter(el => el.checked).map(el => el.value)",
    )
    assert set(checked) == {"vanilla_tc", "gregtech", "forbidden_magic", "magic_bees", "thaumic_tinkerer"}


# --- Connection Helper --------------------------------------------------------


def test_connection_helper_finds_a_chain(live_server, page):
    page.goto(f"{live_server}/connections")
    # <option>s never count as "visible" for wait_for_selector's default
    # actionability check, even once populated -- wait on their count instead.
    page.wait_for_function("() => document.querySelectorAll('#fromSelect option').length > 0")
    page.select_option("#fromSelect", "aer")
    page.select_option("#toSelect", "lux")
    page.fill("#minSteps", "1")
    page.click("#findBtn")
    page.wait_for_selector("#resultChain .chain-item")

    items = page.query_selector_all("#resultChain .chain-item")
    assert len(items) >= 2
    first_name = items[0].query_selector("span").text_content()
    last_name = items[-1].query_selector("span").text_content()
    assert first_name == "Aer"
    assert last_name == "Lux"


# --- Aspect Sources -----------------------------------------------------------


def test_sources_pure_only_filter_hides_impure_items(live_server, page):
    page.goto(f"{live_server}/sources")
    page.wait_for_selector(".source-card")
    page.check("#pureOnly")
    page.wait_for_timeout(100)

    badges = page.eval_on_selector_all(
        ".impurity-badge", "els => els.map(el => el.textContent)"
    )
    assert badges  # the filter shouldn't wipe out every source
    assert all(b == "pure" for b in badges)


def test_sources_good_only_filter_keeps_only_green_items(live_server, page):
    page.goto(f"{live_server}/sources")
    page.wait_for_selector(".source-card")
    page.check("#goodOnly")
    page.wait_for_timeout(100)

    items = page.query_selector_all(".source-item")
    assert items
    assert all("highlight-good" in (i.get_attribute("class") or "") for i in items)


def test_sources_search_filters_cards_by_aspect(live_server, page):
    page.goto(f"{live_server}/sources")
    page.wait_for_selector(".source-card")
    page.fill("#searchBox", "aer")
    page.wait_for_timeout(150)

    names = page.eval_on_selector_all(
        ".source-card-header span", "els => els.map(el => el.textContent)"
    )
    assert names == ["Aer"]


def test_sources_pure_and_good_filters_combine_as_or(live_server, page):
    # Checking both keeps an item if it matches *either* filter, not only
    # items that are both pure and especially-good at once.
    page.goto(f"{live_server}/sources")
    page.wait_for_selector(".source-card")
    page.check("#pureOnly")
    page.check("#goodOnly")
    page.wait_for_timeout(100)

    violation = page.eval_on_selector_all(
        ".source-item",
        """els => els.filter(el =>
            !el.classList.contains('highlight-good') &&
            el.querySelector('.impurity-badge').textContent !== 'pure'
        ).length""",
    )
    assert violation == 0


def test_sources_shows_empty_hint_when_no_aspect_matches_search(live_server, page):
    page.goto(f"{live_server}/sources")
    page.wait_for_selector(".source-card")
    page.fill("#searchBox", "zzznotarealaspect")
    page.wait_for_timeout(150)

    assert page.text_content(".empty-hint") == "No sources match the current filters."


def test_sources_pack_filter_hides_aspects_from_disabled_packs(live_server, page):
    page.goto(f"{live_server}/sources")
    page.wait_for_selector(".source-card")

    def card_names():
        return page.eval_on_selector_all(
            ".source-card-header span", "els => els.map(el => el.textContent)"
        )

    assert "Nebrisum" in card_names()  # gregtech aspect, on by default (GTNH preset)
    page.uncheck("#pack_gregtech")
    page.wait_for_timeout(100)
    assert "Nebrisum" not in card_names()
    assert "Aer" in card_names()  # unaffected vanilla aspect


# --- Nugget Dupe (Metallurgic Perfection) --------------------------------------


def test_nugget_dupe_table_lists_recipes_with_aspect_chips(live_server, page):
    page.goto(f"{live_server}/nugget-dupe")
    page.wait_for_selector("#nuggetDupeBody tr")

    rows = page.query_selector_all("#nuggetDupeBody tr")
    assert len(rows) > 50  # the sheet lists 77 metals

    mithril_row = page.eval_on_selector(
        "#nuggetDupeBody",
        """el => {
            const row = Array.from(el.querySelectorAll('tr')).find(
                tr => tr.querySelector('.metal-name')?.textContent === 'Mithril'
            );
            return Array.from(row.querySelectorAll('.req-chip span')).map(s => s.textContent);
        }""",
    )
    assert mithril_row == ["2× Metallum", "2× Nebrisum", "1× Ordo"]


def test_nugget_dupe_search_filters_rows_by_metal_name(live_server, page):
    page.goto(f"{live_server}/nugget-dupe")
    page.wait_for_selector("#nuggetDupeBody tr")
    page.fill("#searchBox", "gold")
    page.wait_for_timeout(150)

    names = page.eval_on_selector_all(
        "#nuggetDupeBody .metal-name", "els => els.map(el => el.textContent)"
    )
    assert names == ["Gold"]


def test_nugget_dupe_shows_empty_hint_when_no_metal_matches_search(live_server, page):
    page.goto(f"{live_server}/nugget-dupe")
    page.wait_for_selector("#nuggetDupeBody tr")
    page.fill("#searchBox", "zzznotarealmetal")
    page.wait_for_timeout(150)

    assert page.text_content(".empty-hint") == "No metals match the current filters."


def test_nugget_dupe_pack_filter_hides_metals_needing_disabled_pack_aspects(live_server, page):
    page.goto(f"{live_server}/nugget-dupe")
    page.wait_for_selector("#nuggetDupeBody tr")

    def metal_names():
        return page.eval_on_selector_all(
            "#nuggetDupeBody .metal-name", "els => els.map(el => el.textContent)"
        )

    assert "Gallium" in metal_names()  # needs electrum (gregtech)
    page.uncheck("#pack_gregtech")
    page.wait_for_timeout(100)
    assert "Gallium" not in metal_names()
    assert "Aluminum" in metal_names()  # needs only volatus + permutatio (vanilla)


# --- Item Aspect Lookup --------------------------------------------------------


def test_item_lookup_shows_a_capped_purest_first_default_list(live_server, page):
    page.goto(f"{live_server}/item-lookup")
    page.wait_for_selector("#lookupBody tr")

    rows = page.query_selector_all("#lookupBody tr")
    assert len(rows) == 300  # RESULT_CAP
    assert "Showing 300 of" in page.text_content("#resultCount")

    chip_counts = page.eval_on_selector_all(
        "#lookupBody tr", "els => els.map(tr => tr.querySelectorAll('.req-chip').length)"
    )
    assert chip_counts == sorted(chip_counts)  # purest (fewest aspects) first
    assert chip_counts[0] == 1


def test_item_lookup_search_filters_by_item_name(live_server, page):
    page.goto(f"{live_server}/item-lookup")
    page.wait_for_selector("#lookupBody tr")
    page.fill("#searchBox", "bone")
    page.wait_for_timeout(150)

    names = page.eval_on_selector_all(
        "#lookupBody .metal-name", "els => els.map(el => el.textContent)"
    )
    assert names  # non-empty
    assert all("bone" in n.lower() for n in names)


def test_item_lookup_aspect_filter_shows_only_matching_items(live_server, page):
    page.goto(f"{live_server}/item-lookup")
    page.wait_for_selector("#lookupBody tr")
    page.select_option("#aspectFilter", "telum")
    page.wait_for_timeout(150)

    chip_labels = page.eval_on_selector_all(
        "#lookupBody tr", "els => els.map(tr => Array.from(tr.querySelectorAll('.req-chip span')).map(s => s.textContent))"
    )
    assert chip_labels
    assert all(any("Telum" in label for label in row) for row in chip_labels)
    # the purest matches (single-aspect Telum items) sort to the very top
    assert chip_labels[0] == ["1× Telum"]


def test_item_lookup_pack_filter_hides_items_needing_disabled_pack_aspects(live_server, page):
    page.goto(f"{live_server}/item-lookup")
    page.wait_for_selector("#lookupBody tr")
    page.select_option("#aspectFilter", "nebrisum")
    page.wait_for_timeout(150)
    assert "matches" in page.text_content("#resultCount")

    page.uncheck("#pack_gregtech")
    page.wait_for_timeout(150)
    assert page.text_content(".empty-hint") == "No items match the current filters."
