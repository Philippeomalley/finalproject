from django.db import models


class Item(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    cleaned_product_name = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    product_price = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)
    product_discount = models.DecimalField(
        max_digits=20, decimal_places=10, default=0, blank=True)
    product_photo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.product_name
