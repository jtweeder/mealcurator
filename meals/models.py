from django.db import models

meal_time_choices = [
        ('bk', 'Breakfast'),
        ('lu', 'Lunch'),
        ('di', 'Dinner'),
        ('de', 'Dessert'),
        ('sn', 'Snack'),
]
dish_type_choices = [
        ('sp', 'Soup'),
        ('bk', 'Baked Dishes'),
        ('pa', 'Pasta Dishes'),
        ('cu', 'Curry Dishes'),
        ('ca', 'Cassarole Dishes'),
        ('st', 'Stews'),
        ('sa', 'Salad'),
        ('lt', 'Light Dishes'),
        ('na', 'None of those'),
    ]
cooking_method_choices = [
        ('st', 'Stovetop'),
        ('mi', 'Microwave'),
        ('gr', 'Grill'),
        ('ov', 'Oven'),
        ('pr', 'Pressure Cooker'),
        ('af', 'Air Fryer'),
    ]
# Create your models here.


class raw_recipe(models.Model):
    title = models.TextField('Recipie Title')
    rec_url = models.URLField('Recpie URL')
    vegan = models.BooleanField('Vegan')
    vegetarian = models.BooleanField('Vegetarian')
    meal_time = models.CharField('Meal Type',
                                 max_length=2,
                                 choices=meal_time_choices)
    dish_type = models.CharField('Dish Type',
                                 max_length=2,
                                 choices=dish_type_choices)
    cooking_method = models.CharField('Cooking Method',
                                      max_length=2,
                                      choices=cooking_method_choices)
