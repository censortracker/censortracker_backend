# Generated by Django 3.1.14 on 2022-03-25 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_add_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="active",
            field=models.BooleanField(default=False, verbose_name="Active"),
        ),
    ]