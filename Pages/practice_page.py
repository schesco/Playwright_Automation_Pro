from playwright.sync_api import Page


class PracticePage:
    URL = "https://rahulshettyacademy.com/angularpractice/"

    # Locators
    EMAIL_INPUT    = 'input[name="email"]'
    PASSWORD_INPUT = "#exampleInputPassword1"
    CHECKBOX       = "#exampleCheck1"
    DROPDOWN       = "#exampleFormControlSelect1"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def fill_email(self, email: str):
        self.page.fill(self.EMAIL_INPUT, email)

    def fill_password(self, password: str):
        self.page.fill(self.PASSWORD_INPUT, password)

    def check_terms(self):
        self.page.check(self.CHECKBOX)

    def is_checkbox_checked(self) -> bool:
        return self.page.is_checked(self.CHECKBOX)

    def select_dropdown_by_index(self, index: int):
        self.page.select_option(self.DROPDOWN, index=index)

    def fill_login_form(self, email: str, password: str, dropdown_index: int = 0):
        """Füllt das komplette Login Formular aus."""
        self.fill_email(email)
        self.fill_password(password)
        self.check_terms()
        self.select_dropdown_by_index(dropdown_index)
