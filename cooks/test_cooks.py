from django.test import RequestFactory, TransactionTestCase
from django.contrib.auth.models import User
from . import models, views
from .templatetags import cooks_extras
from meals.models import mstr_recipe, meal_item
import uuid


class cook_views(TransactionTestCase):
    reset_sequences = True

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
        self.tst_item = meal_item.objects.create(
                                item_name='testItem',
                                item_location='un'
        )
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
        meals = models.plan_meal.objects.filter(plan=self.tst_plan.pk)
        # Check that above meal and default was added
        self.assertEqual(len(meals), 2)
        self.assertEqual(response.status_code, 302)

    def test_list_add(self):
        data = {'item-qty': 1,
                'item-qty-dec': '1/2',
                'item-uom': 'ea',
                'new-item': 'NewItem'}
        request = self.factory.post('/cooks/add_list', data=data)
        request.user = self.tst_user
        response = views.list_add(request,
                                  self.tst_plan.pk,
                                  meal_id=self.tst_recipe_add.meal_id)
        items = models.plan_list.objects.filter(owner=self.tst_user,
                                                plan=self.tst_plan.pk)
        # Check that above item was added to meal
        self.assertEqual(len(items), 1)
        self.assertEqual(response.status_code, 302)

    def test_val_ret_lstp(self):
        values = [('key', 'value'),
                  ('notkey', 'notvalue')]
        self.assertEqual(cooks_extras.val_ret_lstp(values, 'key'), 'value')

    def test_dec_cleaner(self):
        test_case = [(2.2, '2-1/5'),
                     (3, '3'),
                     (4.99, '5'),
                     (0.25, '1/4'),
                     ]
        for test in test_case:
            self.assertEqual(cooks_extras.dec_cleaner(test[0]), test[1])
        self.assertListEqual(cooks_extras.dec_cleaner(2.5, True), ['2', '1/2'])

    def test_cooks_extras_choice_finder(self):
        sections = cooks_extras.choice_finder('pr', 'sections')
        uom = cooks_extras.choice_finder('ts', 'uoms')
        change = cooks_extras.choice_finder('fx', 'change')

        self.assertEqual(sections, 'Produce')
        self.assertEqual(uom, 'Tsp')
        self.assertEqual(change, 'Fixed')
