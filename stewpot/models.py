from django.db import models
from meals.models import mstr_recipe
from django.contrib.auth.models import User


class meal_posting(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class share_meal(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    meal = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    posting = models.ForeignKey(meal_posting, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title