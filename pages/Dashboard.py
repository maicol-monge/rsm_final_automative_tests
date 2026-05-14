from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://localhost:7274/Users/Dashboard"
        self.welcome_message = (By.CSS_SELECTOR, ".dashboard-header h2")
        self.login_attempts_chart = (By.ID, "loginAttemptsChart")
        self.sessions_chart = (By.ID, "sessionsChart")

    def open_dashboard_page(self):
        self.driver.get(self.url)

    def get_welcome_message(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(self.welcome_message)).text

    def are_charts_visible(self):
        wait = WebDriverWait(self.driver, 10)
        login_chart = wait.until(EC.visibility_of_element_located(self.login_attempts_chart)).is_displayed()
        session_chart = wait.until(EC.visibility_of_element_located(self.sessions_chart)).is_displayed()
        return login_chart and session_chart
