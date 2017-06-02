from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logchan.models import Board, Thread, Post

from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group

from logchan.models import Board, Thread, Post

class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.username = 'admin'
        self.password='imageboard'
        u = User.objects.create_user(username=self.username, password=self.password)
        u.save();
        g = Group.objects.get_or_create(name='Admin')
        g = Group.objects.get(name='Admin')
        g.user_set.add(u)
        self.b = Board(name='Test_board')
        self.b.save()
        self.t = Thread(board=self.b, subject='Test_thread')
        self.t.save()
        self.tt = Thread(board=self.b, subject='Test_thread2')
        self.tt.save()
        self.p = Post(thread=self.t, message="New message test")
        self.p.save()

        self.driver = webdriver.PhantomJS()
        self.baseurl = "http://127.0.0.1:8081/"
        self.driver.get(self.baseurl)
        super(SeleniumTest, self).setUp

    # Close the opened browser at the end of all tests
    #def tearDown(self):
    #    self.driver.quit()

    def test_homepage(self):
        self.assertTrue("Log(chan)" in self.driver.title)

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

    def test_post_get(self):
        self.driver.get('{}board/{}/thread/{}/'.format(self.baseurl, 
            self.b.name, self.t.id))
        post = self.driver.find_element_by_class_name("main-container")
        post = post.find_element_by_id("posts")
        post = post.find_element_by_css_selector("li")
        self.assertEqual(self.p.message, post.text)

    def test_new_post(self):
        self.driver.get('{}board/{}/thread/{}/'.format(self.baseurl, 
            self.b.name, self.tt.id))
        field = self.driver.find_element_by_name("message")
        message = "A new message"
        field.send_keys(message)
        sub = self.driver.find_element_by_id("postForm").find_element_by_css_selector("input[type=submit]")
        sub.click()
        self.driver.find_element_by_id("postForm").find_element_by_css_selector("input[type=submit]").screenshot("screen.png")
        print(Post.objects.all())

        self.driver.get(self.baseurl)
        self.driver.find_element_by_css_selector("nav a").click()
        self.driver.find_element_by_css_selector("article ul a").click()
        print(self.driver.current_url)
        post = self.driver.find_element_by_class_name("main-container")
        post = post.find_element_by_id("posts")
        post = post.find_element_by_css_selector("li")
        self.assertEqual(message, post.text)

    def test_new_thread(self):
        self.driver.find_element_by_css_selector("nav a").click()
        self.assertEqual(True, False)

    def test_login(self):
        self.driver.get('{}/login'.format(self.baseurl))

