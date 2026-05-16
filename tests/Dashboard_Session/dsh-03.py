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

def test_session_lifecycle():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        wait = WebDriverWait(driver, 10)

        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.enter_email("test@example.com")
        login_page.enter_password("Password123!")
        login_page.click_login_button()

        wait.until(EC.url_contains("/Users/Dashboard"))

        navbar = NavbarPage(driver)

        assert navbar.is_session_timer_visible()

        navbar.click_logout()
        wait.until(EC.url_to_be("https://localhost:7274/"))
        assert driver.current_url == "https://localhost:7274/"

        login_page.open_login_page()
        login_page.enter_email("test@example.com")
        login_page.enter_password("Password123!")
        login_page.click_login_button()

        wait.until(EC.url_contains("/Users/Dashboard"))

        print("Waiting for session to expire...")
        time.sleep(60)

        driver.refresh()
        wait.until(EC.url_to_be("https://localhost:7274/"))

        assert driver.current_url == "https://localhost:7274/"
    finally:
        driver.quit()
