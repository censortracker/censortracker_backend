# Generated by Django 3.0.5 on 2021-08-11 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_add_ct_meta_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='ct_meta_info',
        ),
        migrations.AddField(
            model_name='case',
            name='user_agent',
            field=models.TextField(blank=True, null=True, verbose_name='User agent'),
        ),
    ]
