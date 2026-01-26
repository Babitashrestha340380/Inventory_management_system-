# base/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Product, Stock, StockTransfer, PurchaseOrder, DropShipment, DemandForecast

# -------------------------------
# PRODUCT SERIALIZER
# -------------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'description', 'unit_price', 'created_at']


# -------------------------------
# STOCK SERIALIZER
# -------------------------------
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'product', 'quantity', 'reorder_level', 'location']


# -------------------------------
# STOCK TRANSFER SERIALIZER
# -------------------------------
class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = ['id', 'product', 'from_location', 'to_location', 'quantity', 'transfer_date']


# -------------------------------
# PURCHASE ORDER SERIALIZER
# -------------------------------
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'product', 'quantity', 'supplier', 'expected_date', 'received']


# -------------------------------
# DROP SHIPMENT SERIALIZER
# -------------------------------
class DropShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropShipment
        fields = ['id', 'product', 'customer_name', 'address', 'shipped']


# -------------------------------
# DEMAND FORECAST SERIALIZER
# -------------------------------
class DemandForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandForecast
        fields = ['id', 'product', 'month', 'predicted_demand']


# -------------------------------
# USER REGISTER SERIALIZER
# -------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        # Replace spaces with underscores automatically
        return value.replace(" ", "_")

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# -------------------------------
# USER LOGIN SERIALIZER (JWT)
# -------------------------------
class LoginSerializer(TokenObtainPairSerializer):
    """
    Custom login serializer to include username and role (group)
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.groups.first().name if user.groups.exists() else None
        return token
