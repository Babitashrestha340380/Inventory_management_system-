from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# PRODUCT MASTER
# -------------------------------
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------------------
# INVENTORY / STOCK
# -------------------------------
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField(default=10)
    location = models.CharField(max_length=100)

    def needs_reorder(self):
        return self.quantity <= self.reorder_level

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


# -------------------------------
# STOCK TRANSFER
# -------------------------------
class StockTransfer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transfers")
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} from {self.from_location} to {self.to_location}"




# -------------------------------
# DROPSHIPPING
# -------------------------------
class DropShipment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="dropships")
    customer_name = models.CharField(max_length=200)
    address = models.TextField()
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} to {self.customer_name}"


# -------------------------------
# DEMAND FORECASTING
# -------------------------------
class DemandForecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="forecasts")
    month = models.DateField(
        help_text="Use the first day of the month for forecasting (e.g., 2026-01-01)"
    )
    predicted_demand = models.PositiveIntegerField(
        default=0,
        help_text="Predicted quantity for the month"
    )

    class Meta:
        unique_together = ('product', 'month')
        ordering = ['month']

    def __str__(self):
        return f"{self.product.name} - {self.month.strftime('%B %Y')} : {self.predicted_demand}"



# -------------------------------
# PURCHASE ORDER
# -------------------------------
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('FAILED', 'Failed'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_orders")
    quantity = models.PositiveIntegerField()
    supplier = models.CharField(max_length=200)
    expected_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.product.name} - {self.quantity} ({self.status})"


# -------------------------------
# GOODS RECEIVED NOTE (GRN)
# -------------------------------



# -------------------------------
# SALES ORDER
# -------------------------------
from datetime import date

from datetime import date

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('INVOICED', 'Invoiced'),
        ('FAILED', 'Failed')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales_orders")
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    order_date = models.DateField(default=date.today)  # ✅ no auto_now_add

    def __str__(self):
        return f"SO - {self.product.name} ({self.quantity})"


# GOODS RECEIVED NOTE
class GoodsReceivedNote(models.Model):
    purchase_order = models.OneToOneField(PurchaseOrder, on_delete=models.CASCADE, related_name="grn")
    received_quantity = models.PositiveIntegerField()
    received_date = models.DateField(auto_now_add=True)
    matched = models.BooleanField(default=False)      # ✅ GRN matched
    processed = models.BooleanField(default=False)    # ✅ Prevent double-processing

    def __str__(self):
        return f"GRN - {self.purchase_order.product.name} ({self.received_quantity})"


# SALES INVOICE
class SalesInvoice(models.Model):
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name="invoice")
    invoice_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    processed = models.BooleanField(default=False)   # ✅ Prevent double-processing

    def __str__(self):
        return f"Invoice - {self.sales_order.product.name} ({self.quantity})"
