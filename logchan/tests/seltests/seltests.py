from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://docs.djangoproject.com/")
search_box = driver.find_element_by_name("q")
search_box.send_keys("testing")
search_box.send_keys(Keys.RETURN)
assert "Search" in driver.title
# Locate first result in page using css selectors.
result = driver.find_element_by_css_selector("div#search-results a")
result.click()
assert "testing" in driver.title.lower()
driver.quit()
