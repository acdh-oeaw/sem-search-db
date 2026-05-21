from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("archiv", "0003_textsnippet_vector_column_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
              CREATE OR REPLACE FUNCTION update_vector_column()
              RETURNS trigger AS $$
              BEGIN
                NEW.vector_column := to_tsvector(
                  (CASE 
                    WHEN NEW.lang_code = 'deu' THEN 'pg_catalog.german'
                    WHEN NEW.lang_code = 'fra' THEN 'pg_catalog.french'
                    WHEN NEW.lang_code = 'ita' THEN 'pg_catalog.italian'
                    WHEN NEW.lang_code = 'spa' THEN 'pg_catalog.spanish'
                    WHEN NEW.lang_code = 'eng' THEN 'pg_catalog.english'
                    WHEN NEW.lang_code = 'lat' THEN 'pg_catalog.simple'
                    ELSE 'pg_catalog.simple'
                  END)::regconfig,
                  NEW.content
                );
                RETURN NEW;
              END;
              $$ LANGUAGE plpgsql;

              CREATE TRIGGER vector_column_trigger
              BEFORE INSERT OR UPDATE OF content, lang_code
              ON archiv_textsnippet
              FOR EACH ROW EXECUTE PROCEDURE update_vector_column();

              UPDATE archiv_textsnippet SET vector_column = NULL;
            """,
            reverse_sql="""
              DROP TRIGGER IF EXISTS vector_column_trigger
              ON archiv_textsnippet;
              DROP FUNCTION IF EXISTS update_vector_column();
            """,
        ),
    ]
