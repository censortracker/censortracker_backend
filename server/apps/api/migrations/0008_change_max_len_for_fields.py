# Generated by Django 3.0.5 on 2021-08-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_add_client_country_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="client_provider",
            field=models.CharField(
                blank=True, default="", max_length=256, verbose_name="Client provider"
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="client_region",
            field=models.CharField(
                blank=True, default="", max_length=128, verbose_name="Client region"
            ),
        ),
    ]
