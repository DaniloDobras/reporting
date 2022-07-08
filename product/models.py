from django.db import models
from django.utils import timezone


class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    index = models.BigIntegerField(default=0)
    import_id = models.CharField(max_length=255, null=True)
    base_unit_content = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    base_unit_content_uom = models.CharField(max_length=255, null=True)
    no_of_base_units = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    gtin = models.CharField(max_length=255, null=True)
    kollex_product_id = models.CharField(max_length=255, null=True)
    manufacturer = models.CharField(max_length=255, null=True)
    manufacturer_gln = models.CharField(max_length=255, null=True)
    manufacturer_id = models.CharField(max_length=255, null=True)
    flags = models.CharField(max_length=255, null=True)
    list_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    refund_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    gfgh_product_id = models.CharField(max_length=255, null=True)
    sales_unit_pkgg = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    active = models.BigIntegerField(default=0)
