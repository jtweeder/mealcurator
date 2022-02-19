from django.db import models
from django.contrib.auth.models import User
from meals.models import mstr_recipe, meal_time_choices


dow = [
        ('su', 'Sunday'),
        ('mo', 'Monday'),
        ('tu', 'Tuesday'),
        ('we', 'Wednesday'),
        ('th', 'Thursday'),
        ('fr', 'Friday'),
        ('sa', 'Saturday'),
    ]


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
    #meal_day = models.CharField('Day of Week for Meal',
    #                            max_length=2,
    #                            choices=dow)
    #meal_time = models.CharField('Meal Time',
    #                             max_length=2,
    #                             choices=meal_time_choices)

    def __str__(self):
        return self.meal.title

    class Meta:
        unique_together = ['meal', 'plan']