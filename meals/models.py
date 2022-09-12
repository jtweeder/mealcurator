from django.db import models


meal_time_choices = [
        ('bk', 'Breakfast'),
        ('lu', 'Lunch'),
        ('di', 'Dinner'),
        ('sd', 'Side Dish'),
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
        ('sm', 'Smoothie'),
        ('na', 'None of those'),
    ]
cooking_method_choices = [
        ('st', 'Stovetop'),
        ('mi', 'Microwave'),
        ('bl', 'Blender'),
        ('gr', 'Grill'),
        ('ov', 'Oven'),
        ('pr', 'Pressure Cooker'),
        ('sc', 'Slow Cooker'),
        ('af', 'Air Fryer'),
        ('ra', 'Raw/Uncooked'),
        ('ot', 'Other'),
    ]

cook_time_choices = [
        ('20', 'Less Than 20 Minutes'),
        ('40', '20 to 40 Minutes'),
        ('60', '40 to 60 Minutes'),
        ('61', 'Over 60 Minutes'),
    ]

protein_choices = [
        ('be', 'Beef'),
        ('ch', 'Chicken'),
        ('pb', 'Plant Based'),
        ('se', 'Fish/Shellfish'),
        ('pk', 'Pork'),
        ('na', 'None'),
        ('ot', 'Other')
    ]


class raw_recipe(models.Model):
    title = models.CharField('Recipe Title', max_length=255)
    rec_url = models.URLField('Recpie URL', unique=True)
    vegan = models.BooleanField('Vegan')
    vegetarian = models.BooleanField('Vegetarian')
    meal_time = models.CharField('Meal Type',
                                 max_length=2,
                                 choices=meal_time_choices)
    dish_type = models.CharField('Dish Type',
                                 max_length=2,
                                 choices=dish_type_choices)
    protein_type = models.CharField('Main Protein',
                                    max_length=2,
                                    choices=protein_choices,
                                    default='na')
    cooking_method = models.CharField('Cooking Method',
                                      max_length=2,
                                      choices=cooking_method_choices)
    cooking_time = models.CharField('Cooking Time',
                                    max_length=2,
                                    choices=cook_time_choices)
    mstr_flag = models.BooleanField(default=False)
    error_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.rec_url

    class Meta:
        indexes = [
            models.Index(fields=['mstr_flag', 'error_flag'])
        ]


class meal_item(models.Model):
    item_name = models.CharField('Item Name', max_length=255)

    def __str__(self):
        return self.item_name


class mstr_recipe(models.Model):
    meal_id = models.UUIDField(primary_key=True,
                               editable=False)
    title = models.CharField('Recipe Title', max_length=255)
    rec_url = models.URLField('Recipe URL')
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
    cooking_time = models.CharField('Cooking Time',
                                    max_length=2,
                                    choices=cook_time_choices)
    protein_type = models.CharField('Main Protein',
                                    max_length=2,
                                    choices=protein_choices, default='na')
    times_selected = models.PositiveIntegerField('Number of times Selected',
                                                 default=0)
    upvotes = models.PositiveIntegerField('Would Make Again', name='upvote',
                                          default=0)
    downvotes = models.PositiveIntegerField('Would Not Make Again',
                                            name='downvote', default=0)
    # TODO: Make this into another model vs tagging along here                                            
    words = models.JSONField('Found Words', name='found_words', default=None)

    def __str__(self):
        return self.title


class mstr_recipe_list(models.Model):
    meal = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE)
    item = models.ForeignKey(meal_item, on_delete=models.CASCADE)
    qty = models.PositiveBigIntegerField('Quantity', default=1)

    class Meta:
        unique_together = ['meal', 'item']


class recipe_sims(models.Model):
    sim = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE)
    compare = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE,
                                related_name='compare_meal')
    score = models.DecimalField('Simularity Score', 'sim_score', 10, 10)
    affirmed_votes = models.PositiveIntegerField('Agreement Votes', 'agree',
                                                 default=0)
    disagree_votes = models.PositiveIntegerField('Disagreement Votes',
                                                 'disagree', default=0)
