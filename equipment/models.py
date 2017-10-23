from django.db import models
from sitepages.models import ProfImage

# Create your models here.

COUNTRY_LIST = (
    # (ISO ALPHA-2 code, name,),
    ('RU', 'Россия',),
    ('CN', 'Китай',),
    ('BY', 'Белорусия',),
    ('CZ', 'Чехия',),
    ('FI', 'Финляндия',),
    ('FR', 'Франция',),
    ('DE', 'Германия',),
    ('HU', 'Венгрия',),
    ('IT', 'Италия',),
    ('NL', 'Нидерланды',),
    ('NO', 'Норвегия',),
    ('PL', 'Польша',),
    ('ES', 'Испания',),
    ('SE', 'Швеция',),
    ('CH', 'Швейцария',),
    ('TR', 'Турция',),
    ('GB', 'Великобритания',),
    ('US', 'США',),
)    


class StockKeepingUnit(models.Model):
    "Единица товарного учёта"

    sku_name = models.CharField(max_length=16, verbose_name='название')
    sku_display_name = models.CharField(blank=True, max_length=30, verbose_name='отображаемое название', help_text='включая html-тэги типа <sup></sup> и т.п.')

    class Meta():
        verbose_name = 'товарная единица'
        verbose_name_plural = 'товарные единицы'

    def __str__(self):
        return self.sku_name


class PriceCurrency(models.Model):
    "Валюта"

    currency_code = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=30)
    currency_display_name = models.CharField(blank=True, max_length=30)
    currency_exchange_rate = models.DecimalField(default=1, max_digits=8, decimal_places=4)
    is_default = models.BooleanField(default=False)
    
    class Meta():
        verbose_name = 'валюта исчисления'
        verbose_name_plural = 'валюты исчисления'

    def __str__(self):
        return self.currency_name


class BrandName(models.Model):
    "Марка"

    brand_slug = models.SlugField(max_length=20)
    brand_name = models.CharField(max_length=20)
    brand_homeland = models.CharField(max_length=2, choices=COUNTRY_LIST)
    brand_display_name = models.CharField(blank=True, max_length=50)
    brand_logo_img = models.ForeignKey(ProfImage, on_delete=models.PROTECT, related_name='brand_set')
    brand_description = models.TextField(blank=True)

    class Meta():
        verbose_name = 'марка оборудования'
        verbose_name_plural = 'марки оборудования'

    def __str__(self):
        return self.brand_name


class Manufacturer(models.Model):
    "Производитель"

    factory_slug = models.SlugField(max_length=20)
    factory_name = models.CharField(max_length=100)
    factory_homeland = models.CharField(max_length=2, choices=COUNTRY_LIST)
    factory_description = models.TextField(blank=True)

    class Meta():
        verbose_name = 'завод изготовитель'
        verbose_name_plural = 'заводы изготовители'

    def __str__(self):
        return self.factory_name


class EquipmentCategory(models.Model):
    "Категория оборудования, она же каталожный узел"

    ecat_slug = models.SlugField(max_length=30)
    is_published = models.BooleanField(default=False)
    ecat_name = models.CharField(max_length=50)
    ecat_image = models.ForeignKey(ProfImage, on_delete=models.PROTECT, related_name='category_set')
    ecat_description = models.TextField(blank=True)

    class Meta():
        verbose_name = 'категория оборудования'
        verbose_name_plural = 'категории оборудования'

    def __str__(self):
        return self.ecat_name


class BaseProduct(models.Model):
    """Базовый класс товара с набором
    общих свойств и атрибутов"""

    product_slug = models.SlugField(max_length=60)
    is_published = models.BooleanField(default=False)
    vendor_code = models.CharField(max_length=40, verbose_name='артикул')
    product_name = models.CharField(max_length=120, verbose_name='наименование')
    product_fullname = models.TextField(blank=True, verbose_name='полное наименование')
    product_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2, verbose_name='каталожная цена')
    price_unit = models.ForeignKey(StockKeepingUnit, on_delete=models.PROTECT, related_name='+')
    price_currency = models.ForeignKey(PriceCurrency, on_delete=models.PROTECT, related_name='product_set')
    trade_unit = models.ForeignKey(StockKeepingUnit, on_delete=models.PROTECT, related_name='+')
    trade_unit_multiplier = models.PositiveSmallIntegerField(default=1, verbose_name='кратность единицы продажи')

    class Meta():
        abstract = True

    def __str__(self):
        return '{0} . {1}'.format(self.vendor_code, self.product_name)
