# Generated by Django 4.0.1 on 2022-02-05 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0009_alter_mstr_recipe_meal_id'),
        ('cooks', '0002_remove_plan_selected_meals_plan_meals_plan_meal_plan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='meals',
            field=models.ManyToManyField(blank=True, to='meals.mstr_recipe'),
        ),
    ]
