# Generated by Django 2.2.5 on 2019-10-19 15:18

from django.db import migrations, models
import polygon.models


class Migration(migrations.Migration):

    dependencies = [
        ('polygon', '0034_auto_20191019_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='only_pdf',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statement',
            name='pdf_statement',
            field=models.FileField(blank=True, null=True, upload_to=polygon.models.get_statement_folder),
        ),
    ]
