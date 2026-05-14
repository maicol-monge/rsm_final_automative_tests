import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.Login import LoginPage
from pages.Dashboard import DashboardPage

def test_dashboard_data_verification():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Precondition: User is authenticated
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.enter_email("test@example.com") # Use a valid, existing user
    login_page.enter_password("Password123!")
    login_page.click_login_button()
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/Users/Dashboard"))

    dashboard_page = DashboardPage(driver)
    
    # Verification
    assert "Welcome" in dashboard_page.get_welcome_message()
    assert dashboard_page.are_charts_visible()
    
    driver.quit()
