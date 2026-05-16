from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://localhost:7274/Users/Register"
        self.full_name_input = (By.ID, "FullName")
        self.email_input = (By.ID, "Email")
        self.phone_input = (By.ID, "PhoneNumber")
        self.password_input = (By.ID, "Password")
        self.confirm_password_input = (By.ID, "ConfirmPassword")
        self.signup_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.email_error = (By.CSS_SELECTOR, "span[data-valmsg-for='Email']")
        self.password_error = (By.CSS_SELECTOR, "span[data-valmsg-for='Password']")
        self.confirm_password_error = (By.CSS_SELECTOR, "span[data-valmsg-for='ConfirmPassword']")
        self.full_name_error = (By.CSS_SELECTOR, "span[data-valmsg-for='FullName']")
        self.phone_error = (By.CSS_SELECTOR, "span[data-valmsg-for='PhoneNumber']")

    def open_register_page(self):
        self.driver.get(self.url)

    def enter_full_name(self, full_name):
        self.driver.find_element(*self.full_name_input).send_keys(full_name)

    def enter_email(self, email):
        self.driver.find_element(*self.email_input).send_keys(email)

    def enter_phone(self, phone):
        self.driver.find_element(*self.phone_input).send_keys(phone)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def enter_confirm_password(self, confirm_password):
        self.driver.find_element(*self.confirm_password_input).send_keys(confirm_password)

    def accept_terms(self):
        try:
            self.driver.find_element(*self.terms_checkbox).click()
        except:
            pass

    def click_signup_button(self):
        button = self.driver.find_element(*self.signup_button)
        self.driver.execute_script("arguments[0].click();", button)

    def get_error_message(self, field="Email", timeout=10):
        """Wait for and retrieve error message for a specific field"""
        field_error_map = {
            "Email": self.email_error,
            "Password": self.password_error,
            "ConfirmPassword": self.confirm_password_error,
            "FullName": self.full_name_error,
            "PhoneNumber": self.phone_error
        }
        error_locator = field_error_map.get(field, self.email_error)
        wait = WebDriverWait(self.driver, timeout)
        error_element = wait.until(EC.visibility_of_element_located(error_locator))
        return error_element.text.strip()
