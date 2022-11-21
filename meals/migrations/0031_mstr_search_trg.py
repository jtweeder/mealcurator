from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    mdl = apps.get_model('meals', 'mstr_search')
    mdl.objects.update(search_vector=SearchVector('raw_words'))


class Migration(migrations.Migration):

    dependencies = [
        ("meals", "0030_mstr_search_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF raw_words, search_vector
            ON meals_mstr_search
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', raw_words
            );
            UPDATE meals_mstr_search SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON meals_mstr_search;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
