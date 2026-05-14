import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Register import RegisterPage

def test_registration_password_mismatch():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    register_page = RegisterPage(driver)
    
    register_page.open_register_page()
    register_page.enter_full_name("Test User")
    register_page.enter_email("testuser@example.com")
    register_page.enter_phone("1234567890")
    register_page.enter_password("Password123!")
    register_page.enter_confirm_password("Password456!")
    register_page.accept_terms()
    register_page.click_signup_button()
    
    error_message = register_page.get_error_message("ConfirmPassword")
    assert "Please enter the same value again." in error_message
    
    driver.quit()
