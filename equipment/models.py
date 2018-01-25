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
    currency_exchange_rate = models.DecimalField(max_digits=7, decimal_places=4, default=1)
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
    product_description = models.TextField(blank=True, verbose_name='описание')
    product_mass = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='масса, кг')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='каталожная цена')
    price_unit = models.ForeignKey(StockKeepingUnit, on_delete=models.PROTECT, related_name='+')
    price_currency = models.ForeignKey(PriceCurrency, on_delete=models.PROTECT, related_name='product_set')
    trade_unit = models.ForeignKey(StockKeepingUnit, on_delete=models.PROTECT, related_name='+')
    trade_unit_multiplier = models.PositiveSmallIntegerField(default=1, verbose_name='кратность единицы продажи')
    complectation = models.TextField(verbose_name='комплектация')

    class Meta():
        abstract = True

    def __str__(self):
        return '{0} . {1}'.format(self.vendor_code, self.product_name)


class Radiator(BaseProduct):
    """Отопительные приборы - радиаторы, конвекторы, польные конвекторы etc"""

    FORM_TYPE_CHOICES = (
        ('panel', 'Панельный'),
        ('sectn', 'Секционный'),
        ('tubes', 'Трубчатый'),
        ('floor', 'Внутрипольный'),
        ('palce', 'Дворцовый'),
        ('plint', 'Плинтусный'),
        ('ceiln', 'Потолочный'),
    )
    STD_MOUNT_TYPE_CHOICES = (
        ('wallmnt', 'Настенный'),
        ('onfloor', 'Напольный'),
        ('infloor', 'Внутрипольный'),
        ('plinthb', 'Плинтусный'),
        ('ceiling', 'Потолочный'),
    )
    MATERIAL_CHOICES = (
        ('steel', 'Сталь'),
        ('alumn', 'Алюминий'),
        ('goose', 'Чугун'),
        ('coopr', 'Медь'),
        ('bimtl', 'Сталь и алюминий'),
        ('plast', 'Пластик'),
    )
    INTAKE_SIDE_CHOICES (
        ('side', 'Боковое'),
        ('down', 'Нижнее'),
        ('othr', 'Другое'),
    )

    form_type = models.CharField(max_length=5, choices=FORM_TYPE_CHOICES, default='panel', verbose_name='тип радиатора')
    std_mount_type = models.CharField(max_length=7, choices=STD_MOUNT_TYPE_CHOICES, default='wallmnt', verbose_name='стандартное размещение')
    material = models.CharField(max_length=5, choices=MATERIAL_CHOICES, default='steel', verbose_name='материал')
    is_wall_mount = models.BooleanField(default=True, verbose_name='возможность настенного монтажа')
    wall_mount_notes = models.TextField(blank=True, null=True, verbose_name='условия для настенного монтажа')
    is_onfloor_mount = models.BooleanField(default=True, verbose_name='возможность напольного монтажа')
    onfloor_mount_notes = models.TextField(blank=True, null=True, verbose_name='условия для напольного монтажа')
    intake_side = models.CharField(max_length=4, choices=INTAKE_SIDE_CHOICES, default='side', verbose_name='тип подключения')
    intake_axis_space = models.PositiveSmallIntegerField(blank=True, null=True, default=500, verbose_name='межосевое расстояние, мм')


class Boiler(BaseProduct):
    """Котёл водогрейный"""

    FUEL_TYPE_CHOICES = (
        ('gastrad', 'Газовый'),
        ('gascond', 'Газовый конденсационный'),
        ('solidfl', 'Твердотопливный'),
        ('electro', 'Электрический'),
        ('univers', 'Универсальный'),
    )
    CONTROL_TYPE_CHOICES = (
        ('absent', 'Без панели управления'),
        ('manual', 'Ручная панель управления'),
        ('weathr', 'Погодозависимая автоматика'),
    )
    WATER_HEATER_TYPE_CHOICES = (
        ('absent', 'Без контура ГВС'),
        ('stream', 'Проточный теплообменник'),
        ('buffer', 'Встроенный бойлер'),
    )
    BODY_MATERIAL_CHOICES = (
        ('goose', 'Чугун'),
        ('steel', 'Сталь'),
        ('coper', 'Медь'),
        ('alloy', 'Сплав'),
    )
    FLUE_GAS_EXTRACTION_CHOICES = (
        ('ntnd', 'Не требуется'),
        ('atmo', 'Естественная тяга'),
        ('trbo', 'Принудительное дымоудаление'),
    )
    COAXIAL_FLUE_NOZZLE_CHOICES = (
        ('060_100', '60/100 мм'),
        ('080_125', '80/125 мм'),
        ('110_150', '110/150 мм'),
    )

    is_wall_mount = models.BooleanField(default=True, verbose_name='настенный')
    wall_mount_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения о настенном монтаже')
    is_onfloor_mount = models.BooleanField(default=False, verbose_name='напольный')
    onfloor_mount_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения о напольном монтаже')
    fuel_type = models.CharField(max_length=7, choices=FUEL_TYPE_CHOICES, default='gastrad', verbose_name='вид топлива')
    body_material = models.CharField(max_length=5, choices=BODY_MATERIAL_CHOICES, default='steel', verbose_name='материал первичного теплообменника котла')
    water_capacity = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='объем теплообменника, л')
    power_max = models.PositiveSmallIntegerField(verbose_name='масимальная мощность, кВт')
    power_min = models.PositiveSmallIntegerField(verbose_name='минимальная мощность, кВт')
    stage_amount = models.PositiveSmallIntegerField(default=1, verbose_name='количество ступеней')
    flame_modulation = models.BooleanField(default=True, verbose_name='модуляция пламени')
    flue_gas_extraction = models.CharField(max_length=4, choices=FLUE_GAS_EXTRACTION_CHOICES, default='atmo', verbose_name='отвод дымовых газов')
    flue_nozzle_diameter = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='диаметр патрубка дымохода, мм')
    coaxial_flue_nozzle_diameter = models.CharField(blank=True, null=True, choices=COAXIAL_FLUE_NOZZLE_CHOICES, verbose_name='диаметр коаксиального дымохода')
    control_type = models.CharField(max_length=6, choices=CONTROL_TYPE_CHOICES, default='absent', verbose_name='панель управления')
    water_heater_type = models.CharField(max_length=6, choices=WATER_HEATER_TYPE_CHOICES, default='stream', verbose_name='тип контура ГВС')
    water_heater_capacity = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='объём встроенного бойлера, л')
    water_heater_perfomance = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='производительность ГВС, л/мин')
    water_heater_perfomance_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения о производительности ГВС')
    is_external_water_heater_ready = models.BooleanField(default=False, verbose_name='штатное подключение внешнего водонагревателя')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения по электропитанию')
    gas_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='расход газа, куб.м/ч')


class ControlPanel(BaseProduct):
    """Панели управления котлов и контроллеры"""

    is_standalone = models.BooleanField(default=False, verbose_name='можно использовать как самостоятельный контроллер')
    boilers = models.ManyToManyField(Boiler)
    is_automatic = models.BooleanField(default=True, verbose_name='автоматическое регулирование')
    is_weather_depended = models.BooleanField(default=True, verbose_name='погодозависимое управление')
    weather_dependency_notes = models.TextField(blank=True, verbose_name='условия для работы контроллера в погодозависимом режиме')
    is_room_temp_depended = models.BooleanField(default=True, verbose_name='регулирование по комнатной температуре')
    room_temp_dependency_notes = models.TextField(blank=True, verbose_name='условия для работы контроллера по комнатной температуре')
    is_remote_control = models.BooleanField(default=False, verbose_name='возможность дистанционного управления')
    remote_control_notes = models.TextField(blank=True, verbose_name='условия для дистанционного управления')
    is_water_heater_control = models.BooleanField(default=True, verbose_name='управление контуром нагрева воды')
    water_heater_control_notes = models.TextField(blank=True, verbose_name='условия для управления нагревом воды')
    straight_circuits_control = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='количество управляемых прямых контуров')
    straight_circuits_control_notes = models.TextField(blank=True, verbose_name='условия для подключения прямых контуров')
    mixed_circuits_control = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='количество управляемых смесительных контуров')
    mixed_circuits_control_notes = models.TextField(blank=True, verbose_name='условия для подключения смесительных контуров')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения по электропитанию')


class ExtensionControlModule(BaseProduct):
    """Платы расширения, модули, блоки дистанционного управления и термостаты"""

    panels = models.ManyToManyField(ControlPanel)
    is_remote_control = models.BooleanField(default=False, verbose_name='является модулем дистанционного управления')
    is_programmable = models.BooleanField(default=False, verbose_name='возможность программирования')
    programms_count = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='количество программ')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения по электропитанию')


class Sensor(BaseProduct):
    """Датчики для плат, модулей и панелей управления"""

    panels = models.ManyToManyField(ControlPanel)
    modules = models.ManyToManyField(ExtensionControlModule)


class WaterHeater(BaseProduct):
    """Водонагреватели проточные и накопительные"""
    HEATING_TYPE_CHOICES = (
        ('ind', 'Косвенный нагрев'),
        ('gas', 'Газовый'),
        ('elc', 'Электрический'),
    )
    ORIENTATION_CHOICES = (
        ('horz', 'Горизонтальный'),
        ('vert', 'Вертикальный'),
        ('univ', 'Универсальный'),
    )
    CONTROL_PANEL_CHOICES = (
        ('absent', 'Отсутствует'),
        ('manual', 'Ручная'),
        ('electr', 'Электронная')
    )

    heating_type = models.CharField(max_length=3, choices=HEATING_TYPE_CHOICES, default='ind', verbose_name='тип нагревателя')
    is_buffer = models.BooleanField(default=True, verbose_name='накопительный')
    capacity = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='объём, л')
    is_wall_mount = models.BooleanField(default=False, verbose_name='настенный монтаж')
    wall_mount_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения о настенном монтаже')
    is_onfloor_mount = models.BooleanField(delault=True, verbose_name='напольный монтаж')
    onfloor_mount_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения о напольном монтаже')
    orientation = models.CharField(max_length=4, choices=ORIENTATION_CHOICES, default='vert', verbose_name='расположение')
    orientation_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения о расположении')
    coil_square = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, verbose_name='площадь змеевика, кв.м')
    primary_circuit_flow = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2, verbose_name='проток в первичном контуре, куб.м/ч')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения по электропитанию')
    perfomance = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='производительность, л/мин')
    perfomance_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения по производительности')
    full_capacity_heating_time = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, verbose_name='время нагрева, ч')
    heating_time_notes = models.TextField(blank=True, null=True, verbose_name='дополнительные сведения о времени нагрева')
    is_extendable = models.BooleanField(default=True, verbose_name='возможность установки дополнительного оборудования')
    extension_notes = models.TextField(blank=True, null=True, verbose_name='информация о дополнительном оборудовании')
    control_panel = models.CharField(max_length=6, default='absent', verbose_name='панель управления')
    shell_color = models.CharField(max_length=20, verbose_name='цвет')


class HydraulicUnit(BaseProduct):
    """Комплекты штуцеров, крестовин и патрубков для гидравлического соединения"""

    pass
