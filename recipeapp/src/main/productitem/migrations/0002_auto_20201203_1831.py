# Generated by Django 3.1.2 on 2020-12-03 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productitem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='product_price',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
    ]