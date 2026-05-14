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
import base64

def create_valid_png_of_size(file_path, size_in_mb):
    png_base = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO7Z4ZkAAAAASUVORK5CYII="
    )
    target_size = int(size_in_mb * 1024 * 1024)
    payload = png_base + (b"\x00" * max(0, target_size - len(png_base)))
    with open(file_path, 'wb') as f:
        f.write(payload)

def test_upload_max_size_image():
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
    create_valid_png_of_size(image_path, 5) # 5 MB
    
    profile_page.upload_profile_picture(image_path)
    profile_page.click_save_changes()
    
    success_message = profile_page.get_success_message()
    assert "Your profile has been updated successfully!" in success_message
    
    if os.path.exists(image_path):
        os.remove(image_path)
        
    driver.quit()
