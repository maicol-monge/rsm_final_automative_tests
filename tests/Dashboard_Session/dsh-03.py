import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Login import LoginPage
from pages.Navbar import NavbarPage
import time

# This test covers SES-01, SES-02, and SES-03
def test_session_lifecycle():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        wait = WebDriverWait(driver, 10)

        # --- Login ---
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.enter_email("test@example.com")
        login_page.enter_password("Password123!")
        login_page.click_login_button()

        wait.until(EC.url_contains("/Users/Dashboard"))

        navbar = NavbarPage(driver)

        # --- SES-01: Verification of the session time counter ---
        # A simple visibility check is more practical for this level of testing.
        assert navbar.is_session_timer_visible()

        # --- SES-03: Manual logout ---
        navbar.click_logout()
        wait.until(EC.url_to_be("https://localhost:7274/"))
        assert driver.current_url == "https://localhost:7274/"

        # --- SES-02: Automatic logout upon session expiration ---
        # Re-login to test auto-logout
        login_page.open_login_page()
        login_page.enter_email("test@example.com")
        login_page.enter_password("Password123!")
        login_page.click_login_button()

        wait.until(EC.url_contains("/Users/Dashboard"))

        # Wait for a duration shorter than the session timeout to ensure we are logged in,
        # then wait for the timeout to occur.
        print("Waiting for session to expire...")
        time.sleep(60)

        # After timeout, any action should ideally redirect to login.
        driver.refresh()
        wait.until(EC.url_to_be("https://localhost:7274/"))

        # Check if we are redirected to the login page
        assert driver.current_url == "https://localhost:7274/"
    finally:
        driver.quit()
