# Generated by Django 4.0.1 on 2022-02-27 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0020_rename_compare_id_recipe_sims_compare_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='recipe_taxonomy',
        ),
    ]
