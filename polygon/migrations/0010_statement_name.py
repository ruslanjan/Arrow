# Generated by Django 2.2.5 on 2019-10-08 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polygon', '0009_auto_20191008_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='name',
            field=models.CharField(default='Statement', max_length=64),
        ),
    ]
