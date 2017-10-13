from django.db import models

# Create your models here.

class StockKeepingUnit(models.Model):
    "Единица товарного учёта"
    sku_name = models.CharField(max_length=16, verbose_name='название', help_text='должно быть уникальным')
    sku_displayname = models.CharField(max_length=30, verbose_name='отображаемое название', help_text='включая html-тэги типа <sup></sup> и т.п.')
    price_multiplier = models.FloatField(default=1, verbose_name='умножающий коэффициент', help_text='множитель базовой цены товара')
    discount = models.SmallIntegerField(default=0, verbose_name='скидка/наценка', help_text='в процентах, скидка или наценка (если отрицательное значение) для данной единицы')


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
