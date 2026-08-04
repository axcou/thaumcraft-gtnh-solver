"""End-to-end browser tests (Playwright) for behavior that only exists in
the DOM/CSS/JS and can't be exercised by the pure-Python backend tests:
the Aspect Combination tree diagram and its pan/zoom, the Solver page's
canvas/grid-import-export interactions, the shared pack selector, and the
Connection Helper's result chain.
"""

from __future__ import annotations

import json


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

    node_count = page.eval_on_selector(
        "#treeDiagram",
        """el => {
            function count(li) {
                const ul = li.querySelector(':scope > ul');
                if (!ul) return 1;
                return 1 + Array.from(ul.children).reduce((sum, child) => sum + count(child), 0);
            }
            const rootLi = el.querySelector(':scope > ul > li');
            return count(rootLi);
        }""",
    )
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


def test_last_child_keeps_its_vertical_connector(live_server, page):
    # Regression test for `border: 0 none` on :last-child::after deleting
    # the drop-line down to the right child along with the (intentionally
    # removed) outward horizontal stub.
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "lux")

    after_border_left = page.eval_on_selector(
        "#treeDiagram",
        """el => {
            const rootLi = el.querySelector(':scope > ul > li');
            const childUl = rootLi.querySelector(':scope > ul');
            const lastLi = childUl.lastElementChild;
            return getComputedStyle(lastLi, '::after').borderLeftStyle;
        }""",
    )
    assert after_border_left == "solid"


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
    page.goto(f"{live_server}/combinations")
    _select_aspect(page, "lux")
    assert page.eval_on_selector(
        "#treeDiagram", "el => el.querySelector(':scope > ul > li > .tree-box span').textContent"
    ) == "Lux"

    _select_aspect(page, "ignis")
    assert page.eval_on_selector(
        "#treeDiagram", "el => el.querySelector(':scope > ul > li > .tree-box span').textContent"
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
    assert set(checked) == {"vanilla_tc", "gregtech", "forbidden_magic", "magic_bees"}


def test_gtnh_preset_is_checked_by_default_on_load(live_server, page):
    page.goto(f"{live_server}/")
    page.wait_for_selector("#packs input[type=checkbox]")
    checked = page.eval_on_selector_all(
        "#packs input[type=checkbox]",
        "els => els.filter(el => el.checked).map(el => el.value)",
    )
    assert set(checked) == {"vanilla_tc", "gregtech", "forbidden_magic", "magic_bees"}


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


# --- Metallurgic Perfection ---------------------------------------------------


def test_metallurgy_table_lists_recipes_with_aspect_chips(live_server, page):
    page.goto(f"{live_server}/metallurgy")
    page.wait_for_selector("#metallurgyBody tr")

    rows = page.query_selector_all("#metallurgyBody tr")
    assert len(rows) > 50  # the sheet lists 77 metals

    iron_row = page.eval_on_selector(
        "#metallurgyBody",
        """el => {
            const row = Array.from(el.querySelectorAll('tr')).find(
                tr => tr.querySelector('.metal-name')?.textContent === 'Iron'
            );
            return Array.from(row.querySelectorAll('.req-chip span')).map(s => s.textContent);
        }""",
    )
    assert iron_row == ["2× Metallum", "2× Nebrisum", "1× Ordo"]


def test_metallurgy_search_filters_rows_by_metal_name(live_server, page):
    page.goto(f"{live_server}/metallurgy")
    page.wait_for_selector("#metallurgyBody tr")
    page.fill("#searchBox", "gold")
    page.wait_for_timeout(150)

    names = page.eval_on_selector_all(
        "#metallurgyBody .metal-name", "els => els.map(el => el.textContent)"
    )
    assert names == ["Gold"]
