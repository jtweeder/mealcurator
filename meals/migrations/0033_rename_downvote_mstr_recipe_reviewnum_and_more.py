# Generated by Django 4.0.1 on 2023-01-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0032_creative_commons_alter_mstr_recipe_cooking_method_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mstr_recipe',
            old_name='downvote',
            new_name='reviewnum',
        ),
        migrations.RemoveField(
            model_name='mstr_recipe',
            name='upvote',
        ),
        migrations.AddField(
            model_name='mstr_recipe',
            name='reviewsum',
            field=models.PositiveIntegerField(default=0, verbose_name='Reviews'),
        ),
    ]