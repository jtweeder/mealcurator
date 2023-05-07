from django.db import models
from django.contrib.auth.models import User
from meals.models import mstr_recipe, meal_item
from mealcurator import choices


class plan(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Meal Plan Name', max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class plan_meal(models.Model):
    meal = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(plan, on_delete=models.CASCADE,
                             related_name='meals_on_plan')
    date_added = models.DateTimeField(auto_now=True)
    review = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.meal.title

    class Meta:
        unique_together = ['meal', 'plan']


class plan_list(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    meal = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE)
    item = models.ForeignKey(meal_item, on_delete=models.CASCADE)
    qty = models.DecimalField(default=1, max_digits=8, decimal_places=3)
    uom = models.CharField('Unit of Measure', max_length=2,
                           choices=choices.uoms, default='qt')
    got = models.BooleanField(default=False)

    class Meta:
        ordering = ['plan', 'meal', 'item']
