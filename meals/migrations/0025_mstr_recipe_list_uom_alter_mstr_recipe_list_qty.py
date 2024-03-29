# Generated by Django 4.0.1 on 2022-09-17 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0024_meal_item_mstr_recipe_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='mstr_recipe_list',
            name='uom',
            field=models.CharField(choices=[('qt', 'Qty'), ('ml', 'Mililiter'), ('ll', 'Liter'), ('ts', 'Tsp'), ('tb', 'Tbsp'), ('cu', 'Cup'), ('oz', 'Ounzes'), ('lb', 'Pounds')], default='qt', max_length=2, verbose_name='Unit of Measure'),
        ),
        migrations.AlterField(
            model_name='mstr_recipe_list',
            name='qty',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=8),
        ),
    ]
