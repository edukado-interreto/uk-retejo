from django.db import migrations


class Migration(migrations.Migration):
    """
    The `base` app was removed, its only model (FontAwesomeIcon) was used by
    blocks that no longer exist. Its migrations are gone with it, so the table
    is dropped here.
    """

    dependencies = [
        ("core", "0008_alter_homepage_body_alter_homepage_hero_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            "DROP TABLE IF EXISTS base_fontawesomeicon",
            migrations.RunSQL.noop,
        ),
    ]
