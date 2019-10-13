# Generated by Django 2.2.5 on 2019-10-13 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polygon', '0018_auto_20191014_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='verdict',
            field=models.CharField(blank=True, choices=[('OK', 'OK'), ('WA', 'Wrong answer'), ('PE', 'Presentation error'), ('EOF', 'UNEXPECTED_EOF'), ('TLE', 'Time limit exceeded'), ('MLE', 'Memory limit exceeded'), ('RE', 'Runtime error'), ('TE', 'Test error'), ('UC', 'Unknown code')], max_length=64, null=True),
        ),
    ]
