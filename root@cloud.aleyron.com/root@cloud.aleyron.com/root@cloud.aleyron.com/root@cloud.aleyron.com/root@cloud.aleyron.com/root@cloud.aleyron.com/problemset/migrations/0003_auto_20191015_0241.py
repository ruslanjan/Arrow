# Generated by Django 2.2.5 on 2019-10-14 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0002_auto_20191015_0218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problemsettask',
            old_name='is_ready',
            new_name='is_active',
        ),
    ]