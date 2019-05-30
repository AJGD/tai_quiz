"""tests for the 'accounts' app"""
from django.test import TestCase


class SampleTestClass(TestCase):
    """Placeholder test for the 'accounts' app."""
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse((lambda x: x > 0)(-1))

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)