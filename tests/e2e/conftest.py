"""Fixtures for the end-to-end browser tests: a live Flask server and a
Playwright browser/page pair.

Scoped to tests/e2e/ specifically (rather than the whole suite) since
nothing outside this directory needs a real server or a browser.

Browser tests are skipped automatically -- not failed -- on a machine
with no usable Chromium/Edge/Chrome for Playwright to drive.
"""

from __future__ import annotations

import socket
import threading
from typing import Iterator

import pytest
from werkzeug.serving import make_server

from tcsolver.webapp import app


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="session")
def live_server() -> Iterator[str]:
    """Runs the actual Flask app in a background thread for the duration
    of the test session, on its own free port (session-scoped: the app
    holds no per-request server-side state, so sharing it across tests
    is safe)."""
    port = _free_port()
    server = make_server("127.0.0.1", port, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture(scope="session")
def browser():
    playwright_module = pytest.importorskip("playwright.sync_api")
    with playwright_module.sync_playwright() as p:
        last_exc: Exception | None = None
        launched = None
        for channel in ("msedge", "chrome", None):
            try:
                launched = p.chromium.launch(channel=channel, headless=True) if channel else p.chromium.launch(headless=True)
                break
            except Exception as exc:  # noqa: BLE001 - probing multiple channels
                last_exc = exc
        if launched is None:
            pytest.skip(f"No usable browser found for Playwright: {last_exc}")
        try:
            yield launched
        finally:
            launched.close()


@pytest.fixture()
def page(browser):
    page = browser.new_page(viewport={"width": 1500, "height": 1000})
    try:
        yield page
    finally:
        page.close()
