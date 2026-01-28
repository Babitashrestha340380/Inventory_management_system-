from django.contrib import admin
from .models import (
    Product,
    Stock,
    StockTransfer,
    PurchaseOrder,
    DropShipment,
    DemandForecast,
    GoodsReceivedNote,
    SalesOrder,
    SalesInvoice
)

# Already registered:
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(StockTransfer)
admin.site.register(PurchaseOrder)
admin.site.register(DropShipment)
admin.site.register(DemandForecast)

# ⚡ Register missing models for testing signals
admin.site.register(GoodsReceivedNote)
admin.site.register(SalesOrder)
admin.site.register(SalesInvoice)
