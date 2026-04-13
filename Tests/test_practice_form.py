import allure
import logging
import pytest
from Pages.practice_page import PracticePage

logger = logging.getLogger(__name__)

VALID_EMAIL    = "hello@gmail.com"
VALID_PASSWORD = "123456"
EXPECTED_URL   = "https://rahulshettyacademy.com/angularpractice/"


@allure.feature("Navigation")
class TestNavigation:

    @allure.title("Seitentitel ist nicht leer")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_title_is_not_empty(self, practice_page: PracticePage):
        logger.info("Prüfe ob Seitentitel nicht leer ist")
        title = practice_page.get_title()
        logger.info(f"Titel gefunden: {title}")
        assert title != ""

    @allure.title("Korrekte URL geladen")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_correct_url_loaded(self, practice_page: PracticePage):
        logger.info("Prüfe ob korrekte URL geladen wurde")
        url = practice_page.get_url()
        logger.info(f"URL gefunden: {url}")
        assert url == EXPECTED_URL


@allure.feature("Login Formular")
class TestLoginForm:

    @allure.title("Email Feld ausfüllen")
    @allure.severity(allure.severity_level.NORMAL)
    def test_fill_email(self, practice_page: PracticePage):
        logger.info(f"Fülle Email Feld aus: {VALID_EMAIL}")
        practice_page.fill_email(VALID_EMAIL)
        value = practice_page.page.input_value('input[name="email"]')
        logger.info(f"Email Feld Wert: {value}")
        assert value == VALID_EMAIL

    @allure.title("Passwort Feld ausfüllen")
    @allure.severity(allure.severity_level.NORMAL)
    def test_fill_password(self, practice_page: PracticePage):
        logger.info("Fülle Passwort Feld aus")
        practice_page.fill_password(VALID_PASSWORD)
        value = practice_page.page.input_value("#exampleInputPassword1")
        logger.info(f"Passwort Feld Wert: {value}")
        assert value == VALID_PASSWORD

    @allure.title("Checkbox wird angehakt")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkbox_is_checked(self, practice_page: PracticePage):
        logger.info("Hake Checkbox an")
        practice_page.check_terms()
        result = practice_page.is_checkbox_checked()
        logger.info(f"Checkbox Status: {result}")
        assert result is True

    @allure.title("Komplettes Formular ausfüllen")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_form(self, practice_page: PracticePage):
        logger.info("Starte kompletten Formular Test")
        with allure.step("Email ausfüllen"):
            logger.info(f"Email: {VALID_EMAIL}")
            practice_page.fill_email(VALID_EMAIL)

        with allure.step("Passwort ausfüllen"):
            logger.info("Passwort wird gesetzt")
            practice_page.fill_password(VALID_PASSWORD)

        with allure.step("Dropdown auswählen"):
            logger.info("Wähle Dropdown Index 0")
            practice_page.select_dropdown_by_index(0)

        with allure.step("Checkbox anklicken"):
            logger.info("Klicke Checkbox an")
            practice_page.check_terms()

        with allure.step("Ergebnis prüfen"):
            result = practice_page.is_checkbox_checked()
            logger.info(f"Checkbox Status: {result}")
            assert result is True