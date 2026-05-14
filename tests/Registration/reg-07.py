import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Register import RegisterPage

def test_registration_empty_full_name():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    register_page = RegisterPage(driver)
    
    register_page.open_register_page()
    register_page.enter_email("testuser@example.com")
    register_page.enter_phone("1234567890")
    register_page.enter_password("Password123!")
    register_page.enter_confirm_password("Password123!")
    register_page.accept_terms()
    register_page.click_signup_button()
    
    error_message = driver.find_element(By.CSS_SELECTOR, "span[data-valmsg-for='FullName']").text
    assert "This field is required." in error_message
    
    driver.quit()
