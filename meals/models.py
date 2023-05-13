from fractions import Fraction
import requests
import random
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import uuid

from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from mealcurator import choices


class raw_recipe(models.Model):
    title = models.CharField('Recipe Title', max_length=255)
    rec_url = models.URLField('Recpie URL', unique=True)
    vegan = models.BooleanField('Vegan')
    vegetarian = models.BooleanField('Vegetarian')
    meal_time = models.CharField('Meal Type',
                                 max_length=2,
                                 choices=choices.meal_time_choices)
    dish_type = models.CharField('Dish Type',
                                 max_length=2,
                                 choices=choices.dish_type_choices)
    protein_type = models.CharField('Main Protein',
                                    max_length=2,
                                    choices=choices.protein_choices,
                                    default='na')
    cooking_method = models.CharField('Cooking Method',
                                      max_length=2,
                                      choices=choices.cooking_method_choices)
    cooking_time = models.CharField('Cooking Time',
                                    max_length=2,
                                    choices=choices.cook_time_choices)
    mstr_flag = models.BooleanField(default=False)
    error_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.rec_url

    def pull_mstr(self):
        try:
            self.soup = self._make_soup()
            title = self.soup.title.string
            learned_tkns, words = self._make_tkns()
            mstr = mstr_recipe.objects.create(
                    meal_id=uuid.uuid1(),
                    title=title,
                    rec_url=self.rec_url,
                    vegan=self.vegan,
                    vegetarian=self.vegetarian,
                    meal_time=self.meal_time,
                    dish_type=self.dish_type,
                    cooking_method=self.cooking_method,
                    cooking_time=self.cooking_time,
                    protein_type=self.protein_type,
                    found_words=learned_tkns,
                   )
            mstr_search.objects.create(
                meal_id=mstr,
                raw_words=words
            )
            return True

        except ValueError:
            return False

    def _make_soup(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
        ]
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}
        page = requests.get(self.rec_url, headers=headers)
        if not page.ok:
            raise ValueError(f'URL did not resolve to OK: {page.status_code}')
        return BeautifulSoup(page.content, 'html.parser')

    def _make_tkns(self):
        # Returns JSON represtnation of lemented word list
        words = [w for w in word_tokenize(self.soup.get_text().lower())
                 if w.isalpha()]
        raw_tkns = [w for w in words
                    if w not in stopwords.words('english')]
        lemmatizer = WordNetLemmatizer()
        lemented = [lemmatizer.lemmatize(w) for w in raw_tkns]
        return lemented, words

    class Meta:
        indexes = [
            models.Index(fields=['mstr_flag', 'error_flag'])
        ]


class meal_item(models.Model):
    item_name = models.CharField('Item Name', max_length=255)
    item_location = models.CharField('Item Section',
                                     max_length=2,
                                     choices=choices.sections,
                                     default='un')
    poss_duplicate = models.BooleanField('Possible Duplicate', default=False)

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
                                 choices=choices.meal_time_choices)
    dish_type = models.CharField('Dish Type',
                                 max_length=2,
                                 choices=choices.dish_type_choices)
    cooking_method = models.CharField('Cooking Method',
                                      max_length=2,
                                      choices=choices.cooking_method_choices)
    cooking_time = models.CharField('Cooking Time',
                                    max_length=2,
                                    choices=choices.cook_time_choices)
    protein_type = models.CharField('Main Protein',
                                    max_length=2,
                                    choices=choices.protein_choices,
                                    default='na')
    times_selected = models.PositiveIntegerField('Number of times Selected',
                                                 default=0)
    sumreview = models.PositiveIntegerField('Sum of Reviews',
                                            default=0)
    numreview = models.PositiveIntegerField('Number of Reviews',
                                            default=0)
    dummy = models.BooleanField(default=False, null=True)
    # TODO: Make this into another model vs tagging along here
    words = models.JSONField('Found Words', name='found_words', default=None)

    def __str__(self):
        return self.title

    def avg_review(self):
        if self.numreview == 0:
            return 0
        else:
            review = Fraction(self.sumreview/self.numreview).limit_denominator(2)
            return float(review)


class mstr_search(models.Model):
    meal_id = models.OneToOneField(mstr_recipe, on_delete=models.CASCADE,
                                   primary_key=True)
    raw_words = models.TextField('Recipe Text')
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]


class mstr_recipe_list(models.Model):
    meal = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE)
    item = models.ForeignKey(meal_item, on_delete=models.CASCADE)
    qty = models.DecimalField(default=1, max_digits=8, decimal_places=3)
    uom = models.CharField('Unit of Measure', max_length=2,
                           choices=choices.uoms,
                           default='qt')

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


class change_log(models.Model):
    version = models.CharField('Version', max_length=256, primary_key=True)
    implemented = models.DateField()

    def __str__(self):
        return self.version


class changes(models.Model):
    version = models.ForeignKey(change_log, on_delete=models.CASCADE)
    change = models.CharField('Change Type', max_length=2,
                              choices=choices.change)
    change_desc = models.CharField('Change Description', max_length=256)
    entry_date = models.DateField(auto_now_add=True)


class creative_commons(models.Model):
    title = models.CharField(max_length=256)
    internal = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    link_text = models.CharField(max_length=256)
    link = models.URLField()

    def __str__(self):
        return self.title
