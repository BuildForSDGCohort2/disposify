# Generated by Django 3.0.9 on 2020-10-07 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200923_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customermore',
            old_name='collector',
            new_name='collectors',
        ),
    ]
