# Generated by Django 3.0.5 on 2021-08-10 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_change_max_len_for_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="reported",
            field=models.BooleanField(default=False),
        ),
    ]
