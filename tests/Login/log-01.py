import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Login import LoginPage

def test_successful_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login_page = LoginPage(driver)
    
    login_page.open_login_page()
    login_page.enter_email("mjosuemonge23@gmail.com")
    login_page.enter_password("Hola123$")
    login_page.click_login_button()
    
    assert driver.current_url == "https://localhost:7274/Users/Dashboard"
    
    driver.quit()
