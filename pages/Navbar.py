from selenium.webdriver.common.by import By

class NavbarPage:
    def __init__(self, driver):
        self.driver = driver
        self.dashboard_link = (By.XPATH, "//a[contains(@class,'nav-link') and normalize-space()='Dashboard']")
        self.my_profile_link = (By.XPATH, "//a[contains(@class,'nav-link') and normalize-space()='My Profile']")
        self.logout_link = (By.XPATH, "//a[contains(@class,'nav-link') and normalize-space()='Logout']")
        self.session_timer = (By.ID, "session-timer")

    def click_dashboard(self):
        self.driver.find_element(*self.dashboard_link).click()

    def click_my_profile(self):
        self.driver.find_element(*self.my_profile_link).click()

    def click_logout(self):
        self.driver.find_element(*self.logout_link).click()

    def is_session_timer_visible(self):
        return self.driver.find_element(*self.session_timer).is_displayed()
