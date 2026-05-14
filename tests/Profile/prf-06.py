import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.Profile import ProfilePage
from pages.Login import LoginPage
from pages.Navbar import NavbarPage
import os
import time

def test_image_preview_verification():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.enter_email("test@example.com")
    login_page.enter_password("Password123!")
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
    
    initial_src = profile_page.get_image_preview_src()
    
    image_path = "preview_image.png"
    profile_page.upload_profile_picture(image_path)
    
    # Wait a moment for the JavaScript to update the preview
    time.sleep(1)
    
    new_src = profile_page.get_image_preview_src()
    
    assert new_src != initial_src
    assert "blob:" in new_src # The new src should be a local blob URL created by the browser
    
    if os.path.exists(image_path):
        os.remove(image_path)
        
    driver.quit()
