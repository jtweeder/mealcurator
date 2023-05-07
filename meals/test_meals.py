from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from . import models, views
import uuid


class raw_recipe_test(TestCase):

    def create_raw_recipe(self, title="test",
                          rec_url="https://www.mealcurator.com", vegan=False,
                          vegetarian=False, meal_time='bk', dish_type='sp',
                          cooking_method='st', cooking_time='20',
                          mstr_flag=False, error_flag=False):

        return models.raw_recipe.objects.create(title=title,
                                                rec_url=rec_url,
                                                vegan=vegan,
                                                vegetarian=vegetarian,
                                                meal_time=meal_time,
                                                dish_type=dish_type,
                                                cooking_method=cooking_method,
                                                cooking_time=cooking_time,
                                                mstr_flag=mstr_flag,
                                                error_flag=error_flag)

    def setUp(self):
        self.raw_rec = self.create_raw_recipe()

    def test_raw_recipe_find_text(self):
        #  raw_rec = self.create_raw_recipe()
        self.assertTrue(self.raw_rec.pull_mstr())

    def test_raw_recipe_created(self):
        self.assertTrue(isinstance(self.raw_rec, models.raw_recipe))

    def test_raw_recipe_url_found(self):
        self.assertEqual(self.raw_rec.__str__(), self.raw_rec.rec_url)


class mstr_recipe_test(TestCase):

    def create_mstr_recipe(self, meal_id=uuid.uuid1(), title='TestTitle2',
                           rec_url="https://www.mealcurator.com", vegan=False,
                           vegetarian=False, meal_time='bk', dish_type='sp',
                           cooking_method='st', cooking_time='20',
                           times_selected=0, sumreview=0, numreview=0):

        return models.mstr_recipe.objects.create(meal_id=meal_id, title=title,
                                                 rec_url=rec_url, vegan=vegan,
                                                 vegetarian=vegetarian,
                                                 meal_time=meal_time,
                                                 dish_type=dish_type,
                                                 cooking_method=cooking_method,
                                                 cooking_time=cooking_time,
                                                 times_selected=times_selected,
                                                 sumreview=sumreview,
                                                 numreview=numreview,
                                                 found_words="test"
                                                 )

    def setUp(self):
        self.mstr_rec = self.create_mstr_recipe()
        self.factory = RequestFactory()

    def test_mstr_recipe_creation(self):
        self.assertTrue(isinstance(self.mstr_rec, models.mstr_recipe))

    def test_mstr_recipe_name(self):
        self.assertEqual(self.mstr_rec.__str__(), 'TestTitle2')

    def test_blank_review(self):
        self.assertEqual(self.mstr_rec.avg_review(), 0)

    def test_one_review(self):
        (models.mstr_recipe.objects.filter(meal_id=self.mstr_rec.meal_id)
                                   .update(sumreview=1, numreview=2)
         )
        self.assertEqual(models.mstr_recipe.objects.get(
                         meal_id=self.mstr_rec.meal_id).avg_review(),
                         0.5)

    def test_show_recipe(self):
        request = self.factory.get('/browse')
        response = views.show_recipe(request)
        self.assertEqual(response.status_code, 200)


class meal_item_test(TestCase):

    def setUp(self):
        self.new_item = models.meal_item.objects.create(item_name='onions',
                                                        item_location='un',
                                                        poss_duplicate=False)

    def test_item_made(self):
        self.assertEqual(self.new_item.__str__(), 'onions')


class creative_commons_test(TestCase):

    def setUp(self):
        self.new_common = models.creative_commons.objects.create(
                                title='creative_test',
                                internal='test',
                                description='desc',
                                link_text='urltext',
                                link='https://www.google.com'
                          )

    def test_create_common_made(self):
        self.assertEqual(self.new_common.__str__(), 'creative_test')


class meal_views_test(TestCase):

    def setUp(self):
        self.tst_user_staff = User.objects.create_user(
                                          'view_test2',
                                          'views2@mealcurator.com',
                                          'johnpassword',
                                          is_staff=True
        )
        self.tst_user = User.objects.create_user('view_test3',
                                                 'views3@mealcurator.com',
                                                 'johnpassword')

        self.factory = RequestFactory()

    def test_staff_check(self):
        self.assertFalse(views.staff_check(self.tst_user))
        self.assertTrue(views.staff_check(self.tst_user_staff))

    def test_index(self):
        request = self.factory.get('')
        response = views.index(request)
        self.assertEqual(response.status_code, 200)

    def test_howto(self):
        request = self.factory.get('/howto')
        response = views.howto(request)
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        request = self.factory.get('/about')
        response = views.about(request)
        self.assertEqual(response.status_code, 200)

    def test_change_log(self):
        request = self.factory.get('/changelog')
        response = views.change_log(request)
        self.assertEqual(response.status_code, 200)

    def test_creative_commons(self):
        request = self.factory.get('/attribution')
        response = views.creative_commons_credit(request)
        self.assertEqual(response.status_code, 200)

    def test_mstr_lst(self):
        request = self.factory.get('/mstr')

        request.user = self.tst_user_staff
        response = views.mstr_lst(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.tst_user
        response = views.mstr_lst(request)
        self.assertEqual(response.status_code, 302)
