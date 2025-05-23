# Generated by Django 5.2 on 2025-05-13 13:22

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0004_alter_homepage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("hero_block", 8),
                    ("heading_block", 10),
                    ("paragraph_block", 11),
                    ("image_block", 14),
                    ("embed_block", 15),
                ],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"form_classname": "title", "required": True},
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"blank": True, "required": False},
                    ),
                    2: (
                        "wagtail.blocks.DateBlock",
                        (),
                        {"blank": True, "required": False},
                    ),
                    3: ("wagtail.images.blocks.ImageBlock", [], {"blank": True}),
                    4: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {
                            "help_text": "Link to another website page",
                            "required": False,
                        },
                    ),
                    5: (
                        "wagtail.blocks.PageChooserBlock",
                        (),
                        {"help_text": "Link to a page", "required": False},
                    ),
                    6: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Text to display in the button",
                            "required": True,
                        },
                    ),
                    7: (
                        "wagtail.blocks.StructBlock",
                        [[("url", 4), ("page", 5), ("text", 6)]],
                        {"blank": True, "required": False},
                    ),
                    8: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 0),
                                ("dates", 1),
                                ("start_date", 2),
                                ("end_date", 2),
                                ("location", 1),
                                ("background", 3),
                                ("call_to_action", 7),
                            ]
                        ],
                        {},
                    ),
                    9: (
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
                    10: (
                        "wagtail.blocks.StructBlock",
                        [[("heading_text", 0), ("size", 9)]],
                        {},
                    ),
                    11: ("wagtail.blocks.RichTextBlock", (), {"icon": "pilcrow"}),
                    12: ("wagtail.images.blocks.ImageBlock", [], {}),
                    13: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    14: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 12), ("caption", 13), ("attribution", 13)]],
                        {},
                    ),
                    15: (
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
