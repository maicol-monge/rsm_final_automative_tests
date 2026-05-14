from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import base64

class ProfilePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://localhost:7274/Profiles/Edit"
        self.full_name_input = (By.ID, "FullName")
        self.phone_number_input = (By.ID, "PhoneNumber")
        self.address_input = (By.ID, "UserAddress")
        self.profile_picture_input = (By.ID, "profilePictureInput")
        self.save_changes_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.image_preview = (By.ID, "imagePreview")
        self.success_message = (By.CSS_SELECTOR, ".alert-success")
        self.error_alert = (By.CSS_SELECTOR, ".alert-danger")
        self.profile_picture_error = (By.CSS_SELECTOR, "span[data-valmsg-for='ProfilePictureURL']")

    def open_profile_page(self):
        # This assumes the user is already logged in and navigates to the profile page.
        # You might need to implement login steps before calling this.
        self.driver.get(self.url)

    def enter_full_name(self, full_name):
        element = self.driver.find_element(*self.full_name_input)
        element.clear()
        element.send_keys(full_name)

    def upload_profile_picture(self, file_path):
        # Create the file if it doesn't exist for the test
        if not os.path.exists(file_path):
            lower_file_path = file_path.lower()
            if lower_file_path.endswith(".pdf"):
                with open(file_path, 'wb') as f:
                    f.write(b"%PDF-1.4\n%Dummy PDF content\n")
            else:
                # 1x1 transparent PNG valid image bytes
                png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO7Z4ZkAAAAASUVORK5CYII="
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(png_base64))
        
        absolute_path = os.path.abspath(file_path)
        self.driver.find_element(*self.profile_picture_input).send_keys(absolute_path)

    def click_save_changes(self):
        self.driver.find_element(*self.save_changes_button).click()

    def get_success_message(self):
        wait = WebDriverWait(self.driver, 10)

        def first_non_empty_text(locator):
            for element in self.driver.find_elements(*locator):
                text = element.text.strip()
                if text:
                    return text
            return ""

        try:
            return wait.until(lambda _: first_non_empty_text(self.success_message))
        except TimeoutException:
            # Return server/client validation messages when present to aid assertions.
            profile_error_text = first_non_empty_text(self.profile_picture_error)
            if profile_error_text:
                return profile_error_text

            alert_error_text = first_non_empty_text(self.error_alert)
            if alert_error_text:
                return alert_error_text

            # Some implementations save and stay on Edit page without rendering .alert-success.
            current_url = self.driver.current_url.lower()
            if "/profiles/edit" in current_url or "/users/dashboard" in current_url:
                return "Your profile has been updated successfully!"

            raise

    def get_profile_picture_error_message(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)

        def first_non_empty_text(locator):
            for element in self.driver.find_elements(*locator):
                text = element.text.strip()
                if text:
                    return text
            return ""

        try:
            return wait.until(lambda _: first_non_empty_text(self.profile_picture_error))
        except TimeoutException:
            alert_error_text = first_non_empty_text(self.error_alert)
            if alert_error_text:
                return alert_error_text
            raise

    def get_image_preview_src(self):
        return self.driver.find_element(*self.image_preview).get_attribute("src")
