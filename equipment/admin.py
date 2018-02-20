from django.contrib import admin
from .models import Radiator, Pump, PumpControl, Boiler, ControlPanel, ExtensionControlModule, Sensor, WaterHeater, ExpansionVessel, StockKeepingUnit, PriceCurrency, BrandName, Manufacturer, EquipmentCategory

# Register your models here.
admin.site.register(Radiator)
admin.site.register(Pump)
admin.site.register(PumpControl)
admin.site.register(Boiler)
admin.site.register(ControlPanel)
admin.site.register(ExtensionControlModule)
admin.site.register(Sensor)
admin.site.register(WaterHeater)
admin.site.register(ExpansionVessel)
admin.site.register(StockKeepingUnit)
admin.site.register(PriceCurrency)
admin.site.register(BrandName)
admin.site.register(Manufacturer)
admin.site.register(EquipmentCategory)