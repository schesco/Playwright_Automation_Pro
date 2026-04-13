import os
import logging
import pytest
import allure
from playwright.sync_api import sync_playwright
from Pages.practice_page import PracticePage

# ── Ordner automatisch anlegen ────────────────────────────────────────────────
os.makedirs("reports/logs", exist_ok=True)
os.makedirs("reports/allure-results", exist_ok=True)
os.makedirs("reports/videos", exist_ok=True)
os.makedirs("reports/screenshots", exist_ok=True)

# ── Playwright interne Logs unterdrücken ──────────────────────────────────────
logging.getLogger("playwright").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# ── Fehlerstatus speichern ────────────────────────────────────────────────────
failed_tests = set()
failed_classes = set()


def is_ci() -> bool:
    return os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"


# ── Screenshot bei Fehler ─────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        failed_tests.add(item.nodeid)

        # Klasse merken
        if item.cls:
            failed_classes.add(item.cls.__name__)

        # page Objekt holen
        page = item.funcargs.get("page")
        if page is None:
            practice_page = item.funcargs.get("practice_page")
            if practice_page:
                page = practice_page.page

        if page:
            # lokal speichern
            screenshot_path = f"reports/screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)

            # in Allure einbetten
            with open(screenshot_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name="Screenshot bei Fehler",
                    attachment_type=allure.attachment_type.PNG
                )


# ── Pro Test eigene Log-Datei ─────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def test_logger(request):
    test_name = request.node.name
    log_path = f"reports/logs/{test_name}.log"

    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s – %(message)s"
    ))

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

    yield

    root_logger.removeHandler(file_handler)
    file_handler.close()

    with open(log_path, "r", encoding="utf-8") as f:
        allure.attach(
            f.read(),
            name=f"Log – {test_name}",
            attachment_type=allure.attachment_type.TEXT
        )


# ── Browser ───────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser():
    ci = is_ci()
    print(f"\n{'CI/CD Modus' if ci else 'Lokaler Modus'} erkannt")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=ci,
            slow_mo=0 if ci else 500,
            args=[] if ci else ["--start-maximized"]
        )
        yield browser
        browser.close()


# ── Context + Video ───────────────────────────────────────────────────────────
@pytest.fixture(scope="class")
def page(browser, request):
    ci = is_ci()

    context = browser.new_context(
        no_viewport=True,
        record_video_dir="reports/videos/",        # ← immer aufnehmen
        record_video_size={"width": 1280, "height": 720}
    )
    page = context.new_page()
    yield page

    # erst path holen, dann schließen
    video_path = page.video.path() if page.video else None
    context.close()    # ← Video fertig geschrieben

    class_name = request.node.name
    had_failure = class_name in failed_classes or len(failed_tests) > 0

    if video_path and had_failure:
        # Video in Allure einbetten
        with open(video_path, "rb") as f:
            allure.attach(
                f.read(),
                name="Video bei Fehler",
                attachment_type=allure.attachment_type.WEBM
            )
    elif video_path and not had_failure:
        os.remove(video_path)   # ← Video löschen wenn alles grün


# ── Page Object ───────────────────────────────────────────────────────────────
@pytest.fixture(scope="class")
def practice_page(page):
    return PracticePage(page)


# ── Navigate einmal pro Klasse ────────────────────────────────────────────────
@pytest.fixture(scope="class", autouse=True)
def navigate(practice_page):
    practice_page.navigate()