from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=20, null=False, default=0.0)


class Property(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    value = models.CharField(max_length=50, null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='properties',
        null=False)


class SaleOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='customer', null=False)
    date = models.DateTimeField()
    total_sale = models.DecimalField(
        decimal_places=2, max_digits=20, null=False, default=0.0)


class SaleOrderLine(models.Model):
    sale_order = models.ForeignKey(
        SaleOrder, on_delete=models.CASCADE, related_name='sale_order',
        null=False)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product', null=False)
    quantity = models.IntegerField()
    total = models.DecimalField(
        decimal_places=2, max_digits=20, null=False, default=0.0)
