from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/")

   # def tearDown(self):
        #self.driver.quit()

    def test_homepage(self):
        first_board = self.driver.find_element_by_css_selector("nav a")
        first_board.click()
        search_box.send_keys("testing")
        search_box.send_keys(Keys.RETURN)
        assert "Search" in driver.title
        # Locate first result in page using css selectors.
        result = self.driver.find_element_by_css_selector("div#search-results a")
        result.click()
        assert "testing" in self.driver.title.lower()

