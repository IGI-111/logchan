from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from logchan.models import Board, Thread

class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        b = Board(name='Test_board')
        b.save()
        t = Thread(board=b, subject='Test_thread')
        t.save()

        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.baseurl = "http://127.0.0.1:8081/"
        self.driver.get(self.baseurl)
        super(SeleniumTest, self).setUp

    # Close the opened browser at the end of all tests
    def tearDown(self):
        self.driver.quit()

    def test_homepage(self):
        self.assertTrue("Logchan" in self.driver.title)

    def test_board(self):
        first_board = self.driver.find_element_by_css_selector("nav a")
        board_name = first_board.text
        first_board.click()
        self.assertTrue("board" in self.driver.current_url)
        self.assertTrue(board_name in self.driver.current_url)

    def test_thread(self):
        first_board = self.driver.find_element_by_css_selector("nav a")
        board_name = '{}'.format(first_board.text)
        first_board.click()
        first_thread = self.driver.find_element_by_class_name("main-container")
        first_thread = first_thread.find_element_by_css_selector("article ul a")
        thread_name = first_thread.text
        first_thread.click()

        self.assertTrue("board" in self.driver.current_url)
        self.assertTrue("thread" in self.driver.current_url)
        t = Thread.objects.get(board=Board.objects.get(name=board_name), 
            subject=thread_name)
        self.assertTrue('{}'.format(t.id) in self.driver.current_url)
