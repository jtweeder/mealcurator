from django.db import models
import uuid

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
        ('af', 'Air Fryer'),
    ]

cook_time_choices = [
        ('20', 'Less Than 20 Minutes'),
        ('40', '20 to 40 Minutes'),
        ('60', '40 to 60 Minutes'),
        ('61', 'Over 60 Minutes'),
    ]

# Create your models here.


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


class mstr_recipe(models.Model):
    meal_id = models.UUIDField(primary_key=True, default=uuid.uuid1(),
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
    times_selected = models.PositiveIntegerField('Number of times Selected',
                                                 default=0)
    upvotes = models.PositiveIntegerField('Would Make Again', name='upvote',
                                          default=0)
    downvotes = models.PositiveIntegerField('Would Not Make Again',
                                            name='downvote', default=0)
    words = models.JSONField('Found Words', name='found_words', default=None)

    def __str__(self):
        return self.title


class recipe_taxonomy(models.Model):
    taxonomy_id = models.OneToOneField(mstr_recipe, models.CASCADE, 'meal_id',
                                       primary_key=True)
    learned_words = models.JSONField('Learned Taxonomy', name='learned_words',
                                     default=None)
    affirmed_words = models.JSONField('Word Up Votes', name='correct_words',
                                      default=None)
    negative_words = models.JSONField('Word Down Votes', name='wrong_words',
                                      default=None)


class recipe_sims(models.Model):
    sim_id = models.OneToOneField(mstr_recipe, models.CASCADE, 'meal_id')
    compare_id = models.CharField('Comparison Recipe ID', max_length=32)
    score = models.DecimalField('Simularity Score', 'sim_score', 10, 10)
    affirmed_votes = models.PositiveIntegerField('Agreement Votes', 'agree',
                                                 default=0)
    disagree_votes = models.PositiveIntegerField('Disagreement Votes',
                                                 'disagree', default=0)
