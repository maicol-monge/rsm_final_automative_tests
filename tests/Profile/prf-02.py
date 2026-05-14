import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.Profile import ProfilePage
from pages.Login import LoginPage
from pages.Navbar import NavbarPage
import os

def test_upload_valid_profile_picture():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.enter_email("mjosuemonge23@gmail.com")
    login_page.enter_password("Hola123$")
    login_page.click_login_button()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//a[contains(@class,'nav-link') and normalize-space()='My Profile']"
    )))

    navbar_page = NavbarPage(driver)
    navbar_page.click_my_profile()
    wait.until(EC.url_contains("/Profiles/Edit"))
    
    profile_page = ProfilePage(driver)
    
    image_path = "test_image.png"
    profile_page.upload_profile_picture(image_path)
    profile_page.click_save_changes()
    
    success_message = profile_page.get_success_message()
    assert "Your profile has been updated successfully!" in success_message
    
    # Clean up the created file
    if os.path.exists(image_path):
        os.remove(image_path)
        
    driver.quit()
