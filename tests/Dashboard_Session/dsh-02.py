import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.Register import RegisterPage
from pages.Login import LoginPage
from pages.Dashboard import DashboardPage
import random
import string

def generate_random_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"

def test_dashboard_for_new_user():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Precondition: Register a new user
        register_page = RegisterPage(driver)
        new_email = generate_random_email()
        register_page.open_register_page()
        register_page.enter_full_name("New User")
        register_page.enter_email(new_email)
        register_page.enter_phone("1122334455")
        register_page.enter_password("Password123!")
        register_page.enter_confirm_password("Password123!")
        register_page.accept_terms()
        register_page.click_signup_button()

        wait = WebDriverWait(driver, 10)

        # Login as the new user
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.enter_email(new_email)
        login_page.enter_password("Password123!")
        login_page.click_login_button()

        wait.until(EC.url_contains("/Users/Dashboard"))

        # Verification
        dashboard_page = DashboardPage(driver)
        assert "Welcome, New User" in dashboard_page.get_welcome_message()
        assert dashboard_page.are_charts_visible()
        # Further checks could be done on chart data if accessible, e.g., via API or JS variables
    finally:
        driver.quit()
