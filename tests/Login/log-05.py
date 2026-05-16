import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Login import LoginPage

def test_uppercase_email():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login_page = LoginPage(driver)
    
    login_page.open_login_page()
    login_page.enter_email("USER@example.com")
    login_page.enter_password("Password123!")
    login_page.click_login_button()
    
    assert driver.current_url == "https://localhost:7274/Users/Dashboard"
    
    driver.quit()
