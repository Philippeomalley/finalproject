# Generated by Django 3.1.2 on 2020-12-02 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20201130_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_rating',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
    ]
