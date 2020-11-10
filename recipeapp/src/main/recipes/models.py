from django.db import models


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255, unique=True)
    recipe_total = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)

    # models.DecimalField(
    # 'price', max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.recipe_name
