# Generated by Django 2.2.5 on 2019-09-26 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polygon', '0002_auto_20190926_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='solution',
            field=models.TextField(),
        ),
    ]
