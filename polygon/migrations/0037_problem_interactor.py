# Generated by Django 2.2.5 on 2019-10-23 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polygon', '0036_auto_20191023_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='interactor',
            field=models.TextField(blank=True, default=''),
        ),
    ]
