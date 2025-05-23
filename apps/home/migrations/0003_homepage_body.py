# Generated by Django 5.1.8 on 2025-04-29 09:16

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("heading_block", 2),
                    ("paragraph_block", 3),
                    ("image_block", 6),
                    ("embed_block", 7),
                ],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"form_classname": "title", "required": True},
                    ),
                    1: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "blank": True,
                            "choices": [
                                ("", "Select a heading size"),
                                ("h2", "H2"),
                                ("h3", "H3"),
                                ("h4", "H4"),
                            ],
                            "required": False,
                        },
                    ),
                    2: (
                        "wagtail.blocks.StructBlock",
                        [[("heading_text", 0), ("size", 1)]],
                        {},
                    ),
                    3: ("wagtail.blocks.RichTextBlock", (), {"icon": "pilcrow"}),
                    4: ("wagtail.images.blocks.ImageBlock", [], {}),
                    5: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 4), ("caption", 5), ("attribution", 5)]],
                        {},
                    ),
                    7: (
                        "wagtail.embeds.blocks.EmbedBlock",
                        (),
                        {
                            "help_text": "Insert a URL to embed. For example, https://www.youtube.com/watch?v=SGJFWirQ3ks",
                            "icon": "media",
                        },
                    ),
                },
                help_text="Use this section to list UK pros.",
            ),
        ),
    ]
