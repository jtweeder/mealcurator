from django.db import models
from meals.models import mstr_recipe
from django.contrib.auth.models import User


class share_meal(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    meal = models.ForeignKey(mstr_recipe, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
