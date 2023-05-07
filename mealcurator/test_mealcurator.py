from django.test import TestCase
from . import helperfuncs, choices


class mealcurator(TestCase):

    def setUp(self):
        self.blank = helperfuncs.check_blank('', 'testdefault')
        self.non_blank = helperfuncs.check_blank('TestNonBlank', 'testdefault')

    def test_check_blank_blank(self):
        self.assertEqual(self.blank, 'testdefault')

    def test_check_blank_nonblank(self):
        self.assertEqual(self.non_blank, 'TestNonBlank')

    def test_choices(self):
        choice_lists = [(name, lst) for name, lst in choices.__dict__.items()
                        if isinstance(lst, list)]
        for name, lst in choice_lists:
            keys = [item[0] for item in lst]
            set_keys = set(keys)
            # Check each list is unique keys
            self.assertEqual(len(keys), len(set_keys))
