"""Tests"""
from django.test import LiveServerTestCase
from selenium import webdriver

from quizzes.models import Quiz, Player


class FilterTestClass(LiveServerTestCase):
    """Filter Test"""

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.player = Player.objects.create(username="Bobby")
        Quiz.objects.create(
            name="Cinema",
            author=self.player,
            category='TRAVEL',
            topic='Spain'
        )

    def tearDown(self):
        self.selenium.quit()

    def test_name_filter_page(self):
        """test filtering by name"""
        selenium = self.selenium
        # Opening the link we want to test
        inserted_text = "Cinema"
        amount = len(Quiz.objects.filter(name=inserted_text))
        selenium.get(self.live_server_url + '/quizzes/')
        # find the form element
        name = selenium.find_element_by_id('name')
        submit = selenium.find_element_by_xpath("//input[@name='Filter'][@type='submit']")

        # Fill the form with data
        name.send_keys(inserted_text)

        # submitting the form
        submit.click()

        # check the returned result
        assert selenium.page_source.count(inserted_text) == amount

    def test_author_filter_page(self):
        """test filtering by author"""
        selenium = self.selenium
        inserted_text = 'Bobby'
        # Opening the link we want to test
        player = Player.objects.get(username=inserted_text)
        amount = len(Quiz.objects.filter(author=player))
        selenium.get(self.live_server_url + '/quizzes/')
        # find the form element
        author = selenium.find_element_by_id('author')
        submit = selenium.find_element_by_xpath("//input[@name='Filter'][@type='submit']")

        # Fill the form with data
        author.send_keys(inserted_text)

        # submitting the form
        submit.click()

        # check the returned result
        assert (selenium.page_source.count(inserted_text) - 1) == amount

    def test_category_filter_page(self):
        """test filtering by category"""
        selenium = self.selenium
        inserted_text = 'TRAVEL'
        # Opening the link we want to test
        amount = len(Quiz.objects.filter(category=inserted_text))
        selenium.get(self.live_server_url + '/quizzes/')
        # find the form element
        category = selenium.find_element_by_id('category')
        submit = selenium.find_element_by_xpath("//input[@name='Filter'][@type='submit']")

        # Fill the form with data
        category.send_keys(inserted_text)

        # submitting the form
        submit.click()

        # check the returned result
        assert (selenium.page_source.count(inserted_text) - 1) == amount

    def test_topic_filter_page(self):
        """test filtering by topic"""
        selenium = self.selenium
        inserted_text = 'Spain'
        # Opening the link we want to test
        amount = len(Quiz.objects.filter(topic=inserted_text))
        selenium.get(self.live_server_url + '/quizzes/')
        # find the form element
        topic = selenium.find_element_by_id('topic')
        submit = selenium.find_element_by_xpath("//input[@name='Filter'][@type='submit']")

        # Fill the form with data
        topic.send_keys(inserted_text)

        # submitting the form
        submit.click()

        # check the returned result
        assert selenium.page_source.count(inserted_text) == amount

    def test_topic_and_author_filter_page(self):
        """test filtering by topic"""
        selenium = self.selenium
        inserted_topic = 'Spain'
        inserted_author = 'Bobby'
        # Opening the link we want to test
        player = Player.objects.get(username=inserted_author)
        # find the form element
        # Opening the link we want to test
        amount = len(Quiz.objects.filter(topic=inserted_topic, author=player))
        selenium.get(self.live_server_url + '/quizzes/')
        # find the form element
        topic = selenium.find_element_by_id('topic')
        author = selenium.find_element_by_id('author')
        submit = selenium.find_element_by_xpath("//input[@name='Filter'][@type='submit']")

        # Fill the form with data
        topic.send_keys(inserted_topic)
        author.send_keys(inserted_author)

        # submitting the form
        submit.click()

        # check the returned result
        assert selenium.page_source.count(inserted_topic) + selenium.page_source \
            .count(inserted_author) >= amount


class CreateLinkTestClass(LiveServerTestCase):
    """Check if home page create link exists for not logged in user"""

    def setUp(self):
        self.selenium = webdriver.Firefox()

    def tearDown(self):
        self.selenium.quit()

    def test_link(self):
        """test existing of link"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url)

        # check the returned result
        assert selenium.page_source.count("Logout") == 0


class CreateLinkForLoggedTestClass(LiveServerTestCase):
    """Check if home page create link exists for logged user"""

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.player = Player.objects.create(username="Bobby", password="Zachannasian")

    def tearDown(self):
        self.selenium.quit()

    def test_link(self):
        """test existing the link"""
        selenium = self.selenium

        selenium.get(self.live_server_url + '/account/login')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('//button[text()="Login"]')

        # Fill the form with data
        username.send_keys('Bobby')
        password.send_keys('Zachannasian')

        # submitting the form
        submit.click()

        print(selenium.current_url)
        selenium.get(self.live_server_url)
        print(selenium.current_url)

        assert selenium.page_source.count("Logout") != 0
