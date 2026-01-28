# base/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ✅ EXPLICIT IMPORTS (THIS FIXES THE ERROR)
from base.views import (
    
    ProductViewSet,
    StockViewSet,
    StockTransferViewSet,
    PurchaseOrderViewSet,
    DropShipmentViewSet,
    DemandForecastViewSet,
    GoodsReceivedNoteViewSet,
    SalesOrderViewSet,
    SalesInvoiceViewSet,
    RegisterView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stock', StockViewSet)
router.register(r'transfers', StockTransferViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)
router.register(r'dropship', DropShipmentViewSet)
router.register(r'forecast', DemandForecastViewSet)
router.register(r'grn', GoodsReceivedNoteViewSet)
router.register(r'sales-orders', SalesOrderViewSet)
router.register(r'sales-invoices', SalesInvoiceViewSet)


urlpatterns = [
    path('', include(router.urls)),
      path('register/', RegisterView.as_view(), name='register'),

    # Inventory APIs
]
