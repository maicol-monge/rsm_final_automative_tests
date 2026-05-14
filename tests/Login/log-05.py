import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Login import LoginPage

def test_login_empty_password():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login_page = LoginPage(driver)
    
    login_page.open_login_page()
    login_page.enter_email("test@example.com")
    login_page.click_login_button()
    
    error_message = driver.find_element(By.CSS_SELECTOR, "span[data-valmsg-for='Password']").text
    assert "The password is required." in error_message
    
    driver.quit()
