from django.http import HttpRequest
from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver

# Create your tests here.
from django.core.urlresolvers import resolve
from django.utils.datetime_safe import datetime

from blogpost.models import Blogpost
from blogpost.views import index, view_post


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertIn(b'<title>Welcome to my blog</title>', response.content)


class BlogpostTest(TestCase):
    def test_blogpost_create_with_view(self):
        Blogpost.objects.create(title='hello', author='admin', slug='this_is_a_test', body='This is a blog',
                                posted=datetime.now)
        response = self.client.get('/blog/this_is_a_test.html')
        self.assertIn(b'This is a blog', response.content)

    def test_blogpost_url_resolves_to_blog_post_view(self):
        found = resolve('/blog/this_is_a_test.html')
        self.assertEqual(found.func, view_post)

    def test_blogpost_create_with_show_in_homepage(self):
        Blogpost.objects.create(title='hello2', author='admin2', slug='this_is_a_test2', body='This is a blog',
                                posted=datetime.now)
        response = self.client.get('/')
        self.assertIn(b'This is a blog', response.content)


class HomepageTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome('/Users/lz/Virtualenvs/BlogEnv/selenium/webdriver/chrome/chromedriver')
        self.selenium.maximize_window()
        super(HomepageTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(HomepageTestCase, self).tearDown()

    def test_visit_homepage(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/")
        )

        self.assertIn("Welcome to my blog", self.selenium.title)


class BlogpostDetailCase(LiveServerTestCase):
    def setUp(self):
        Blogpost.objects.create(
            title='hello',
            author='admin',
            slug='this_is_a_test',
            body='This is a blog',
            posted=datetime.now
        )

        self.selenium = webdriver.Chrome('/Users/lz/Virtualenvs/BlogEnv/selenium/webdriver/chrome/chromedriver')
        self.selenium.maximize_window()
        super(BlogpostDetailCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(BlogpostDetailCase, self).tearDown()

    def test_visit_blog_post(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/blog/this_is_a_test.html")
        )

        self.assertIn("hello", self.selenium.title)

class BlogpostFromHomepageCase(LiveServerTestCase):
    def setUp(self):
        Blogpost.objects.create(
            title='hello',
            author='admin',
            slug='this_is_a_test',
            body='This is a blog',
            posted=datetime.now
        )

        self.selenium = webdriver.Chrome('/Users/lz/Virtualenvs/BlogEnv/selenium/webdriver/chrome/chromedriver')
        self.selenium.maximize_window()
        super(BlogpostFromHomepageCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(BlogpostFromHomepageCase, self).tearDown()

    def test_visit_blog_post(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/")
        )

        self.selenium.find_element_by_link_text("hello").click()
        self.assertIn("hello", self.selenium.title)
