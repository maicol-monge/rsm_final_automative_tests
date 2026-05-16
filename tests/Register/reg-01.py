import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Register import RegisterPage
import random
import string

def generate_random_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"

def test_successful_registration():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    register_page = RegisterPage(driver)
    
    register_page.open_register_page()
    register_page.enter_full_name("Test User Selenium")
    register_page.enter_email(generate_random_email())
    register_page.enter_phone("1234567890")
    register_page.enter_password("Password123!")
    register_page.enter_confirm_password("Password123!")
    register_page.accept_terms()
    register_page.click_signup_button()
    
    assert driver.current_url == "https://localhost:7274/"
    
    driver.quit()
