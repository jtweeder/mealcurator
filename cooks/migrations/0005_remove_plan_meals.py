# Generated by Django 4.0.1 on 2022-02-18 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooks', '0004_remove_plan_meal_meal_day_remove_plan_meal_meal_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='meals',
        ),
    ]
