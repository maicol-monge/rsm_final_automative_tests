import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Register import RegisterPage

def test_registration_short_password():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    register_page = RegisterPage(driver)
    
    register_page.open_register_page()
    register_page.enter_full_name("Test User")
    register_page.enter_email("testuser@example.com")
    register_page.enter_phone("1234567890")
    register_page.enter_password("Pass")
    register_page.enter_confirm_password("Pass")
    register_page.accept_terms()
    register_page.click_signup_button()
    
    error_message = register_page.get_error_message("Password")
    assert error_message == "Please enter at least 8 characters."
    
    driver.quit()
