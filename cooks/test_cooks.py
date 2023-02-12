from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from . import models, views
from meals.models import mstr_recipe
import uuid


class cook_views(TestCase):
    def setUp(self):
        self.tst_user = User.objects.create_user('view_test',
                                                 'views@mealcurator.com',
                                                 'johnpassword')
        self.tst_plan = models.plan.objects.create(owner=self.tst_user,
                                                   name='Test Meal Plan')
        self.tst_recipe = mstr_recipe.objects.create(
                                        meal_id=uuid.uuid1(),
                                        title='Cook Test Recipe',
                                        rec_url="https://www.mealcurator.com",
                                        vegan=False,
                                        vegetarian=False,
                                        meal_time='bk',
                                        dish_type='sp',
                                        cooking_method='st',
                                        cooking_time='20',
                                        times_selected=0,
                                        sumreview=0,
                                        numreview=0,
                                        found_words="test"
        )
# TODO: Make test suite that adds above in order

        self.tst_recipe_add = mstr_recipe.objects.create(
                                        meal_id=uuid.uuid1(),
                                        title='Cook Test Recipe Add',
                                        rec_url="https://www.mealcurator.com",
                                        vegan=False,
                                        vegetarian=False,
                                        meal_time='bk',
                                        dish_type='sp',
                                        cooking_method='st',
                                        cooking_time='20',
                                        times_selected=0,
                                        sumreview=0,
                                        numreview=0,
                                        found_words="test"
        )
# TODO: Make test item
        self.tst_plan_meal = models.plan_meal.objects.create(
                                        meal=self.tst_recipe,
                                        plan=self.tst_plan,
        )
        self.factory = RequestFactory()

    def test_cook_profile(self):
        request = self.factory.get('/cooks/register/welcome')
        request.user = self.tst_user
        response = views.cook_profile(request)
        self.assertEqual(response.status_code, 200)

    def test_view_plans(self):
        request = self.factory.get('/cooks/viewplans')
        request.user = self.tst_user
        response = views.view_plans(request)
        self.assertEqual(response.status_code, 200)

    def test_plan_create(self):
        self.assertEqual(self.tst_plan.__str__(), 'Test Meal Plan')

    def test_view_plan(self):
        request = self.factory.get('/cooks/viewplans')
        request.user = self.tst_user
        response = views.view_plan(request, self.tst_plan.pk,
                                   4, self.tst_recipe.meal_id)
        self.assertEqual(response.status_code, 200)

    def test_view_plan_list(self):
        request = self.factory.get('/cooks/list')
        request.user = self.tst_user
        response = views.view_plan(request, self.tst_plan.pk)
        self.assertEqual(response.status_code, 200)

    def test_view_plan_add(self):
        request = self.factory.get('/cooks/mod_plan', follow=True)
        request.user = self.tst_user
        response = views.add_meal_to_plan(request,
                                          self.tst_plan.pk,
                                          self.tst_recipe_add.meal_id)
        self.assertEqual(response.status_code, 200)
        