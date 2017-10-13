from django.db import models

# Create your models here.

class StockKeepingUnit(models.Model):
    "Единица складского учёта товара"
    sku_name = models.CharField(max_length=16, verbose_name='название единицы измерения')
    sku_displayname = models.CharField(max_length=30, verbose_name='отображаемое название с html-тэгами')
    price_multiplier = models.FloatField(default=1, verbose_name='умножающий коэффициент')


class BrandName(models.Model):
    "Марка"
    pass


class Manufacturer(models.Model):
    "Производитель"
    pass


class BaseProduct(models.Model):
    """Базовый класс товара с набором
    общих свойств и атрибутов"""

    vendor_code = models.CharField(max_length=40, verbose_name='артикул')
    product_name = models.CharField(max_length=120, verbose_name='наименование')
    product_fullname = models.TextField(blank=True, verbose_name='полное наименование')

    class Meta():
        abstract = True
