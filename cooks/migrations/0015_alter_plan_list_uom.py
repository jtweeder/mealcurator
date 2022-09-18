# Generated by Django 4.0.1 on 2022-09-18 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooks', '0014_alter_plan_list_options_plan_list_uom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan_list',
            name='uom',
            field=models.CharField(choices=[('qt', ''), ('ts', 'Tsp'), ('tb', 'Tbsp'), ('cu', 'Cup'), ('oz', 'Ounces'), ('lb', 'Pounds'), ('ml', 'Milliliter'), ('ll', 'Liter')], default='qt', max_length=2, verbose_name='Unit of Measure'),
        ),
    ]