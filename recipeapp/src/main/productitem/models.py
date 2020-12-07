from django.db import models


class Item(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    product_price = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)

    # models.DecimalField(
    # 'price', max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.product_name
