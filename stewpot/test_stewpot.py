from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from . import models, views
from meals.models import mstr_recipe
import uuid


class share_meal(TestCase):
    def setUp(self):
        self.tst_user = User.objects.create_user('john',
                                            'lennon@thebeatles.com',
                                            'johnpassword')
        self.tst_recipe = mstr_recipe.objects.create(meal_id=uuid.uuid1(),
                                        title='TestTitle2',
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
        self.share_meal = (models.share_meal
                           .objects.create(title='ShareTest',
                                           creator=self.tst_user,
                                           text='shared meal test',
                                           meal=self.tst_recipe)
                           )

        self.factory = RequestFactory()

    def test_share_meal(self):
        self.assertTrue(isinstance(self.share_meal, models.share_meal))

    def test_share_start(self):
        request = self.factory.get('/share/save')
        request.user = self.tst_user
        response = views.start_share(request, self.tst_recipe.meal_id)
        self.assertEqual(response.status_code, 200)
