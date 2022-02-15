from turtle import down
from django.test import TestCase
from .models import raw_recipe, mstr_recipe
import uuid


class raw_recipe_test(TestCase):

    def create_raw_recipe(self, title="test",
                          rec_url="https://www.mealcurator.com", vegan=False,
                          vegetarian=False, meal_time='bk', dish_type='sp',
                          cooking_method='st', cooking_time='20',
                          mstr_flag=False, error_flag=False):

        return raw_recipe.objects.create(title=title, rec_url=rec_url,
                                         vegan=vegan, vegetarian=vegetarian,
                                         meal_time=meal_time,
                                         dish_type=dish_type,
                                         cooking_method=cooking_method,
                                         cooking_time=cooking_time,
                                         mstr_flag=mstr_flag,
                                         error_flag=error_flag)

    def test_raw_recipe_creation(self):
        raw_rec = self.create_raw_recipe()
        self.assertTrue(isinstance(raw_rec, raw_recipe))
        self.assertEqual(raw_rec.__str__(), raw_rec.rec_url)


class mstr_recipe_test(TestCase):

    def create_mstr_recipe(self, meal_id=uuid.uuid1(), title='TestTitle2',
                           rec_url="https://www.mealcurator.com", vegan=False,
                           vegetarian=False, meal_time='bk', dish_type='sp',
                           cooking_method='st', cooking_time='20',
                           times_selected=0, upvotes=0, downvotes=0):

        return mstr_recipe.objects.create(meal_id=meal_id, title=title,
                                          rec_url=rec_url, vegan=vegan,
                                          vegetarian=vegetarian,
                                          meal_time=meal_time,
                                          dish_type=dish_type,
                                          cooking_method=cooking_method,
                                          cooking_time=cooking_time,
                                          times_selected=times_selected,
                                          upvote=upvotes,
                                          downvote=downvotes,
                                          found_words="test"
                                          )

    def test_mstr_recipe_creation(self):
        mstr_rec = self.create_mstr_recipe()
        self.assertTrue(isinstance(mstr_rec, mstr_recipe))
        self.assertEqual(mstr_rec.__str__(), mstr_rec.title)
