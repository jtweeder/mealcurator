from django.test import TestCase
from . import helperfuncs


class helpers(TestCase):

    def setUp(self):
        self.blank = helperfuncs.check_blank('', 'testdefault')
        self.non_blank = helperfuncs.check_blank('TestNonBlank', 'testdefault')

    def test_check_blank_blank(self):
        self.assertEqual(self.blank, 'testdefault')

    def test_check_blank_nonblank(self):
        self.assertEqual(self.non_blank, 'TestNonBlank')
