# Generated by Django 4.0.1 on 2024-02-04 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0036_mstr_recipe_ai_recipe_raw_recipe_ai_recipe'),
        ('stewpot', '0004_ai_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ai_html',
            name='meal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meals.mstr_recipe'),
        ),
    ]
