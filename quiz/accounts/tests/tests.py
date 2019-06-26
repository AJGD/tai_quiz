"""Tests for 'accounts' - sub-application responsible for registering users"""
from django.test import LiveServerTestCase
from selenium import webdriver


class AccountTestCase(LiveServerTestCase):
    """Testing a simple registration case that should be successful"""

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        """test simple successful registration case"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/account/signup/')
        # find the form element
        username = selenium.find_element_by_id('id_username')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_xpath('//button[text()="Sign up"]')

        # Fill the form with data
        username.send_keys('some username')
        password1.send_keys('123456')
        password2.send_keys('123456')

        # submitting the form
        submit.click()

        # check the returned result
        assert 'Username' in selenium.page_source
