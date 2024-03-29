# Generated by Django 4.0.1 on 2022-01-24 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_mstr_recipe_alter_raw_recipe_title_recipe_taxonomy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='raw_recipe',
            name='cooking_time',
            field=models.CharField(choices=[('20', 'Less Than 20 Minutes'), ('40', '20 to 40 Minutes'), ('60', '40 to 60 Minutes'), ('61', 'Over 60 Minutes')], default='un', max_length=2, verbose_name='Cooking Time'),
            preserve_default=False,
        ),
    ]
