# Generated by Django 3.1.2 on 2020-12-15 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20201214_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='diet',
        ),
        migrations.DeleteModel(
            name='Diet',
        ),
    ]