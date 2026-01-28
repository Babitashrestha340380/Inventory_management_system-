# base/views.py
from rest_framework import viewsets, generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User

from .models import GoodsReceivedNote, Product, SalesInvoice, SalesOrder, Stock, StockTransfer, PurchaseOrder, DropShipment, DemandForecast
from .serializers import (
    GoodsReceivedNoteSerializer,
    ProductSerializer,
    SalesInvoiceSerializer,
    SalesOrderSerializer,
    StockSerializer,
    StockTransferSerializer,
    PurchaseOrderSerializer,
    DropShipmentSerializer,
    DemandForecastSerializer,
    RegisterSerializer,
    LoginSerializer,
)

# -------------------------------
# PRODUCT
# -------------------------------
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Stock, StockTransfer, PurchaseOrder, DropShipment, DemandForecast
from .serializers import (
    ProductSerializer,
    StockSerializer,
    StockTransferSerializer,
    PurchaseOrderSerializer,
    DropShipmentSerializer,
    DemandForecastSerializer,
)

# -------------------------------
# PRODUCT
# -------------------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'sku']  # You can add more fields if needed

# -------------------------------
# STOCK
# -------------------------------
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'location', 'quantity']

# -------------------------------
# STOCK TRANSFER
# -------------------------------
class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'from_location', 'to_location', 'transfer_date']

# -------------------------------
# PURCHASE ORDER
# -------------------------------
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'supplier', 'status', 'expected_date']  # use 'status' instead of 'received'


# -------------------------------
# DROPSHIP
# -------------------------------
class DropShipmentViewSet(viewsets.ModelViewSet):
    queryset = DropShipment.objects.all()
    serializer_class = DropShipmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'customer_name', 'shipped']

# -------------------------------
# DEMAND FORECAST
# -------------------------------
class DemandForecastViewSet(viewsets.ModelViewSet):
    queryset = DemandForecast.objects.all()
    serializer_class = DemandForecastSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'month', 'predicted_demand']


# -------------------------------
# REGISTER USER (Admin Only)
# -------------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]  # Only admin can register new users

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "username": user.username,
            "email": user.email,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


# -------------------------------
# LOGIN USER
# -------------------------------
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class GoodsReceivedNoteViewSet(viewsets.ModelViewSet):
    queryset = GoodsReceivedNote.objects.all()
    serializer_class = GoodsReceivedNoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['purchase_order', 'received_date']


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'customer_name', 'status', 'order_date']


class SalesInvoiceViewSet(viewsets.ModelViewSet):
    queryset = SalesInvoice.objects.all()
    serializer_class = SalesInvoiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sales_order', 'invoice_date']