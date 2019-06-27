"""Tests"""

from django.test import LiveServerTestCase
from selenium import webdriver

from quizzes.models import Quiz, Player, Question


class EditButtonClass(LiveServerTestCase):
    """Edit button redirections Test"""

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.player = Player.objects.create(username="Bobby")
        self.quiz = Quiz.objects.create(
            name="Cinema",
            author=self.player,
            category='TRAVEL',
            topic='Spain'
        )
        self.question_title = Question.objects.create(
            question_text="_ _ _ _ _ _ _ _ _ pochodza z ziemi",
            answer="Ziemniak",
            author=self.player,
            quiz=self.quiz,
            article_id=1213,
            type="Title"
        )
        self.question_stats = Question.objects.create(
            question_text="How many times was the article 'Purée' viewed in the month of 2019-5?",
            answer="1000",
            author=self.player,
            quiz=self.quiz,
            article_id=1214,
            type="Stats"
        )

    def tearDown(self):
        self.selenium.quit()

    def test_button_edit_title(self):
        """test button redirection to title question"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/quizzes/' + str(self.quiz.id) + '/questions')
        # find the form element
        submit = selenium.find_element_by_id("title_button_" + str(self.question_title.id))

        # submitting the form
        submit.click()

        # check the returned result
        assert self.selenium.current_url == self.live_server_url + '/create_question_title/' \
               + str(self.question_title.id) + "/" + str(self.question_title.article_id)

    def test_button_edit_stat(self):
        """test button redirection to statistics question"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/quizzes/' + str(self.quiz.id) + '/questions')
        # find the form element
        submit = selenium.find_element_by_id("stat_button_" + str(self.question_stats.id))

        # submitting the form
        submit.click()

        # check the returned result
        assert self.selenium.current_url == self.live_server_url + '/create_question_stat/' \
               + str(self.question_stats.id) + "/" + str(self.question_stats.article_id)
