from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooks', '0016_alter_plan_list_uom'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Meal Plan Description'),
        ),
    ]
