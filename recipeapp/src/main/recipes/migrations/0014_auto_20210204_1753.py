# Generated by Django 3.1.2 on 2021-02-04 17:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0013_recipe_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='users',
            field=models.ManyToManyField(related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]
