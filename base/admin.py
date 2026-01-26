from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Product,
    Stock,
    StockTransfer,
    PurchaseOrder,
    DropShipment,
    DemandForecast
)

admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(StockTransfer)
admin.site.register(PurchaseOrder)
admin.site.register(DropShipment)
admin.site.register(DemandForecast)
