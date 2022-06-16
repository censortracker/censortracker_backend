# Generated by Django 3.0.5 on 2020-04-20 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="domain",
            name="client_ip",
            field=models.GenericIPAddressField(
                blank=True, null=True, verbose_name="Client IP"
            ),
        ),
    ]
