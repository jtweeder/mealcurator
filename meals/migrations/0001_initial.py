# Generated by Django 4.0.1 on 2022-01-17 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='raw_recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Recipie Title')),
                ('rec_url', models.URLField(verbose_name='Recpie URL')),
                ('vegan', models.BooleanField(verbose_name='Vegan')),
                ('vegetarian', models.BooleanField(verbose_name='Vegetarian')),
                ('meal_time', models.CharField(choices=[('bk', 'Breakfast'), ('lu', 'Lunch'), ('di', 'Dinner'), ('de', 'Dessert'), ('sn', 'Snack')], max_length=2, verbose_name='Meal Type')),
                ('dish_type', models.CharField(choices=[('sp', 'Soup'), ('bk', 'Baked Dishes'), ('pa', 'Pasta Dishes'), ('cu', 'Curry Dishes'), ('ca', 'Cassarole Dishes'), ('st', 'Stews'), ('sa', 'Salad'), ('lt', 'Light Dishes'), ('na', 'None of those')], max_length=2, verbose_name='Dish Type')),
                ('cooking_method', models.CharField(choices=[('st', 'Stovetop'), ('mi', 'Microwave'), ('gr', 'Grill'), ('ov', 'Oven'), ('pr', 'Pressure Cooker'), ('af', 'Air Fryer')], max_length=2, verbose_name='Cooking Method')),
            ],
        ),
    ]
