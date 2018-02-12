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

GEAR_SIZE_CHOICES = (
    ('1/8', '1/8``',),
    ('1/4', '1/4``',),
    ('3/8', '3/8``',),
    ('1/2', '1/2``',),
    ('3/4', '3/4``',),
    ('1/1', '1``',),
    ('5/4', '1 1/4``',),
    ('3/2', '1 1/2``',),
    ('2/1', '2``',),
)

DN_SIZE_CHOICES = (
    ('10', '10',),
    ('16', '16',),
    ('20', '20',),
    ('25', '15',),
    ('32', '32',),
    ('40', '40',),
    ('50', '50',),
    ('63', '63',),
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
    ecat_image = models.ForeignKey(ProfImage, on_delete=models.SET_NULL, null=True, related_name='category_set')
    ecat_description = models.TextField(blank=True, null=True)
    ecat_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='ecat_childrens')

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
    price_currency = models.ForeignKey(PriceCurrency, on_delete=models.PROTECT, related_name='+')
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
        ('panel', 'Панельный',),
        ('sectn', 'Секционный',),
        ('tubes', 'Трубчатый',),
        ('floor', 'Внутрипольный',),
        ('palce', 'Дворцовый',),
        ('plint', 'Плинтусный',),
        ('ceiln', 'Потолочный',),
    )
    MOUNT_TYPE_CHOICES = (
        ('wallmnt', 'Настенный',),
        ('onfloor', 'Напольный',),
        ('infloor', 'Внутрипольный',),
        ('plinthb', 'Плинтусный',),
        ('ceiling', 'Потолочный',),
    )
    MATERIAL_CHOICES = (
        ('steel', 'Чёрная сталь',),
        ('alumn', 'Алюминий',),
        ('goose', 'Чугун',),
        ('coopr', 'Медь',),
        ('bimtl', 'Биметалл сталь/алюминий',),
        ('plast', 'Пластик',),
    )
    INTAKE_SIDE_CHOICES = (
        ('side', 'Боковое',),
        ('down', 'Нижнее',),
        ('othr', 'Другое',),
    )

    form_type = models.CharField(max_length=5, choices=FORM_TYPE_CHOICES, default='panel', verbose_name='тип радиатора')
    mount_type = models.CharField(max_length=7, choices=MOUNT_TYPE_CHOICES, default='wallmnt', verbose_name='стандартное размещение')
    mount_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='информация о монтаже')
    material = models.CharField(max_length=5, choices=MATERIAL_CHOICES, default='steel', verbose_name='материал')
    intake_side = models.CharField(max_length=4, choices=INTAKE_SIDE_CHOICES, default='side', verbose_name='тип подключения')
    intake_axis_space = models.PositiveSmallIntegerField(blank=True, null=True, default=500, verbose_name='межосевое расстояние, мм')
    height = models.PositiveSmallIntegerField(verbose_name='высота, мм')
    length = models.PositiveSmallIntegerField(verbose_name='длина, мм')
    depth = models.PositiveSmallIntegerField(verbose_name='глубина (ширина), мм')
    section_count = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='количество секций')
    output_power = models.PositiveSmallIntegerField(verbose_name='мощность, Вт')
    water_capacity = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2, verbose_name='объём воды в радиаторе, л')
    connection_gear_size = models.CharField(blank=True, null=True, max_length=3, choices=GEAR_SIZE_CHOICES, verbose_name='размер присоединительной резьбы')
    connection_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='информация о присоединении', help_text='резьба наружняя/внутренняя/НГ и уплотнение')
    op_overpressure = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='максимальное рабочее давление, бар')
    is_builtin_regulation = models.BooleanField(default=False, verbose_name='встроенный терморегулятор')
    regulation_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='информация о встроенном терморегуляторе')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по электропитанию')


class Pump(BaseProduct):
    """Насосы самые разные"""

    PURPOSE_CHOICES = (
        ('circulation', 'Циркуляционный',),
        ('groundwater', 'Дренажный',),
        ('submercible', 'Погружной/колодезный',),
        ('boreholesbm', 'Скважинный',),
        ('selfpriming', 'Самовсасывающий',),
        ('pressurebst', 'Повысительный',),
        ('sewagesbmrc', 'Фекальный',),
    )

    purpose = models.CharField(max_length=11, choices=PURPOSE_CHOICES, default='circulation', verbose_name='назначение')
    head_max = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='максимальный напор, м')
    head_min = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='минимальный напор, м')
    head_optimal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='напор при максимальном КПД, м')
    flow_max = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='максимальный расход, куб.м/ч')
    flow_min = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='минимальный расход, куб.м/ч')
    flow_optimal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='расход при максимальном КПД, куб.м/ч')
    electonic_regulation = models.BooleanField(default=False, verbose_name='частотное регулирование')
    flow_switch = models.BooleanField(default=False, verbose_name='наличие поплавка')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по электропитанию')


class PumpControl(BaseProduct):
    """Шкаф управления насосами"""

    pumps = models.ManyToManyField(Pump)
    overamperage = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='допустимый ток, А')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по электропитанию')


class Boiler(BaseProduct):
    """Котёл водогрейный"""

    MOUNT_TYPE_CHOICES = (
        ('wallmnt', 'Настенный',),
        ('onfloor', 'Напольный',),
    )
    FUEL_TYPE_CHOICES = (
        ('gastrad', 'Газовый',),
        ('gascond', 'Газовый конденсационный',),
        ('solidfl', 'Твердотопливный',),
        ('electro', 'Электрический',),
        ('univers', 'Универсальный',),
    )
    CONTROL_TYPE_CHOICES = (
        ('absent', 'Без панели управления',),
        ('manual', 'Ручная панель управления',),
        ('weathr', 'Погодозависимая автоматика',),
    )
    WATER_HEATER_TYPE_CHOICES = (
        ('absent', 'Без контура ГВС',),
        ('stream', 'Проточный теплообменник',),
        ('buffer', 'Встроенный бойлер',),
    )
    BODY_MATERIAL_CHOICES = (
        ('goose', 'Чугун',),
        ('steel', 'Сталь',),
        ('coper', 'Медь',),
        ('alloy', 'Сплав',),
    )
    FLUE_GAS_EXTRACTION_CHOICES = (
        ('ntnd', 'Не требуется',),
        ('atmo', 'Естественная тяга',),
        ('trbo', 'Принудительное дымоудаление',),
    )
    COAXIAL_FLUE_NOZZLE_CHOICES = (
        ('060_100', '60/100 мм',),
        ('080_125', '80/125 мм',),
        ('110_150', '110/150 мм',),
    )

    mount_type = models.CharField(max_length=7, choices=MOUNT_TYPE_CHOICES, default='wallmnt', verbose_name='тип монтажа')
    fuel_type = models.CharField(max_length=7, choices=FUEL_TYPE_CHOICES, default='gastrad', verbose_name='вид топлива')
    body_material = models.CharField(max_length=5, choices=BODY_MATERIAL_CHOICES, default='steel', verbose_name='материал первичного теплообменника котла')
    primary_op_overpressure = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='максимальное рабочее давление, бар')
    output_power_max = models.PositiveSmallIntegerField(verbose_name='масимальная мощность, кВт')
    output_power_min = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='минимальная мощность, кВт')
    power_stage_amount = models.PositiveSmallIntegerField(default=1, verbose_name='количество ступеней')
    flame_modulation = models.BooleanField(default=True, verbose_name='модуляция пламени')
    flue_gas_extraction = models.CharField(max_length=4, choices=FLUE_GAS_EXTRACTION_CHOICES, default='atmo', verbose_name='отвод дымовых газов')
    flue_nozzle_diameter = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='диаметр патрубка дымохода, мм')
    coaxial_flue_nozzle_diameter = models.CharField(blank=True, null=True, max_length=7, choices=COAXIAL_FLUE_NOZZLE_CHOICES, verbose_name='диаметр коаксиального дымохода')
    control_type = models.CharField(max_length=6, choices=CONTROL_TYPE_CHOICES, default='absent', verbose_name='панель управления')
    wh_type = models.CharField(max_length=6, choices=WATER_HEATER_TYPE_CHOICES, default='stream', verbose_name='тип контура ГВС')
    wh_capacity = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='объём встроенного бойлера, л')
    wh_perfomance = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='производительность ГВС, л/мин')
    wh_perfomance_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения о производительности ГВС')
    wh_op_overpressure = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='максимальное давление в системе ГВС, бар')
    is_external_water_heater_ready = models.BooleanField(default=False, verbose_name='штатное подключение внешнего водонагревателя')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по электропитанию')
    gas_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='расход газа, куб.м/ч')
    height = models.PositiveSmallIntegerField(verbose_name='высота, мм')
    width = models.PositiveSmallIntegerField(verbose_name='ширина, мм')
    depth = models.PositiveSmallIntegerField(verbose_name='глубина, мм')


class ControlPanel(BaseProduct):
    """Панели управления котлов и контроллеры"""

    is_standalone = models.BooleanField(default=False, verbose_name='можно использовать как самостоятельный контроллер')
    boilers = models.ManyToManyField(Boiler, blank=True)
    is_automatic = models.BooleanField(default=True, verbose_name='автоматическое регулирование')
    is_weather_depended = models.BooleanField(default=True, verbose_name='погодозависимое управление')
    weather_dependency_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='условия для работы контроллера в погодозависимом режиме')
    is_room_temp_depended = models.BooleanField(default=True, verbose_name='регулирование по комнатной температуре')
    room_temp_dependency_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='условия для работы контроллера по комнатной температуре')
    is_remote_control = models.BooleanField(default=False, verbose_name='возможность дистанционного управления')
    remote_control_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='условия для дистанционного управления')
    is_water_heater_control = models.BooleanField(default=True, verbose_name='управление контуром нагрева воды')
    water_heater_control_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='условия для управления нагревом воды')
    straight_circuits_control = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='количество управляемых прямых контуров')
    straight_circuits_control_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='условия для подключения прямых контуров')
    mixed_circuits_control = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='количество управляемых смесительных контуров')
    mixed_circuits_control_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='условия для подключения смесительных контуров')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по электропитанию')
    height = models.PositiveSmallIntegerField(verbose_name='высота, мм')
    width = models.PositiveSmallIntegerField(verbose_name='ширина, мм')
    depth = models.PositiveSmallIntegerField(verbose_name='глубина, мм')


class ExtensionControlModule(BaseProduct):
    """Платы расширения, модули, блоки дистанционного управления и термостаты"""

    panels = models.ManyToManyField(ControlPanel, blank=True)
    radiators = models.ManyToManyField(Radiator, blank=True)
    is_remote_control = models.BooleanField(default=False, verbose_name='является модулем дистанционного управления')
    is_programmable = models.BooleanField(default=False, verbose_name='возможность программирования')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по электропитанию')
    height = models.PositiveSmallIntegerField(verbose_name='высота, мм')
    width = models.PositiveSmallIntegerField(verbose_name='ширина, мм')
    depth = models.PositiveSmallIntegerField(verbose_name='глубина, мм')


class Sensor(BaseProduct):
    """Датчики для плат, модулей и панелей управления"""

    panels = models.ManyToManyField(ControlPanel, blank=True)
    modules = models.ManyToManyField(ExtensionControlModule, blank=True)
    pumpcontrols = models.ManyToManyField(PumpControl, blank=True)


class WaterHeater(BaseProduct):
    """Водонагреватели проточные и накопительные"""
    HEATING_TYPE_CHOICES = (
        ('ind', 'Косвенный нагрев',),
        ('gas', 'Газовый',),
        ('elc', 'Электрический',),
    )
    ORIENTATION_CHOICES = (
        ('horz', 'Горизонтальный',),
        ('vert', 'Вертикальный',),
        ('univ', 'Универсальный',),
    )
    CONTROL_PANEL_CHOICES = (
        ('absent', 'Отсутствует',),
        ('manual', 'Ручная',),
        ('electr', 'Электронная',),
    )

    heating_type = models.CharField(max_length=3, choices=HEATING_TYPE_CHOICES, default='ind', verbose_name='тип нагревателя')
    is_buffer = models.BooleanField(default=True, verbose_name='накопительный')
    capacity = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='объём, л')
    is_wall_mount = models.BooleanField(default=False, verbose_name='настенный монтаж')
    wall_mount_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения о настенном монтаже')
    is_onfloor_mount = models.BooleanField(default=True, verbose_name='напольный монтаж')
    onfloor_mount_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения о напольном монтаже')
    orientation = models.CharField(max_length=4, choices=ORIENTATION_CHOICES, default='vert', verbose_name='расположение')
    orientation_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения о расположении')
    primary_op_overpressure = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='максимальное рабочее давление в первичном контуре, бар')
    wh_op_overpressure = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='максимальное давление в системе ГВС, бар')
    perfomance = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='производительность, л/мин')
    perfomance_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по производительности')
    electric_power_consumption = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2, verbose_name='потребляемая электрическая мощность, кВт')
    voltage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='напряжение питания, В')
    voltage_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения по электропитанию')
    full_capacity_heating_time = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, verbose_name='время нагрева, ч')
    heating_time_notes = models.CharField(blank=True, null=True, max_length=250, verbose_name='дополнительные сведения о времени нагрева')
    control_panel = models.CharField(max_length=6, default='absent', verbose_name='панель управления')
    color = models.CharField(max_length=20, verbose_name='цвет')
    height = models.PositiveSmallIntegerField(verbose_name='высота, мм')
    width = models.PositiveSmallIntegerField(verbose_name='ширина, мм')
    depth = models.PositiveSmallIntegerField(verbose_name='глубина, мм')


class ExpansionVessel(BaseProduct):
    """Расширительные баки для отопления и ГВС"""

    PURPOSE_CHOICES = (
        ('heating', 'Система отопления/охлаждения',),
        ('waterss', 'Система водоснабжения',),
    )
    ORIENTATION_CHOICES = (
        ('horz', 'Горизонтальный',),
        ('vert', 'Вертикальный',),
        ('univ', 'Универсальный',),
    )

    purpose = models.CharField(max_length=7, choices=PURPOSE_CHOICES, default='heating', verbose_name='назначение')
    nominal_volume = models.PositiveSmallIntegerField(verbose_name='номинальный объём, л')
    useful_volume = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='полезный объём, л')
    op_temperature = models.PositiveSmallIntegerField(verbose_name='допустимая температура, град.С')
    op_overpressure = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='максимальное рабочее давление, бар')
    gas_inlet_pressure = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='предустановленное давление воздуха в мембране, бар')
    is_changeable_membrane = models.BooleanField(default=False, verbose_name='заменяемая мембрана')
    foot_construction = models.BooleanField(default=False, verbose_name='ножки для напольной установки')
    orientation = models.CharField(max_length=4, choices=ORIENTATION_CHOICES, verbose_name='расположение')
    connection_gear_size = models.CharField(max_length=3, choices=GEAR_SIZE_CHOICES, verbose_name='размер присоединительной резьбы')
    color = models.CharField(max_length=20, verbose_name='цвет')
    diameter = models.PositiveSmallIntegerField(verbose_name='диаметр, мм')
    height = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='высота, мм')
    length = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='длина, мм')
