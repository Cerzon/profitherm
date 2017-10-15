from django.db import models

# Create your models here.

class StockKeepingUnit(models.Model):
    "Единица товарного учёта"
    sku_name = models.CharField(max_length=16, verbose_name='название')
    sku_displayname = models.CharField(max_length=30, verbose_name='отображаемое название', help_text='включая html-тэги типа <sup></sup> и т.п.')

    class Meta():
        verbose_name = 'товарная единица'
        verbose_name_plural = 'товарные единицы'


class PriceCurrency(models.Model):
    "Валюта"
    pass


class BrandName(models.Model):
    "Марка"
    pass


class ManufacturerHomeland(models.Model):
    "Страна производитель"
    pass


class EquipmentCategory(models.Model):
    "Категория оборудования"
    pass


class BaseProduct(models.Model):
    """Базовый класс товара с набором
    общих свойств и атрибутов"""

    vendor_code = models.CharField(max_length=40, verbose_name='артикул')
    product_name = models.CharField(max_length=120, verbose_name='наименование')
    product_fullname = models.TextField(blank=True, verbose_name='полное наименование')
    product_price = models.FloatField(verbose_name='каталожная цена')
    price_unit = models.ForeignKey(StockKeepingUnit, on_delete=models.PROTECT, related_name='+')
    price_currency = models.ForeignKey(PriceCurrency, on_delete=models.PROTECT, related_name='product_set')
    trade_unit = models.ForeignKey(StockKeepingUnit, on_delete=models.PROTECT, related_name='+')
    trade_unit_multiplier = models.PositiveSmallIntegerField(default=1, verbose_name='кратность единицы продажи')

    class Meta():
        abstract = True
