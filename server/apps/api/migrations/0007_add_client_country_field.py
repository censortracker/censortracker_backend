# Generated by Django 3.0.5 on 2021-06-17 12:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_allow_blank_fields"),
        ("api", "0006_auto_20200814_1335"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="client_country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.Country",
            ),
        ),
    ]
