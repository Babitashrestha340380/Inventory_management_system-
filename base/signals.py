from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.conf import settings

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

# -----------------------------
# CONFIGURABLE MAIN WAREHOUSE
# -----------------------------
DEFAULT_WAREHOUSE = getattr(settings, "DEFAULT_WAREHOUSE", "Main Warehouse")


# ---------------------------------
# CREATE DEFAULT GROUPS & PERMISSIONS
# ---------------------------------
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Automatically creates user groups and assigns permissions
    after migrations are applied.
    """

    # CREATE GROUPS
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    manager_group, _ = Group.objects.get_or_create(name="InventoryManager")
    logistics_group, _ = Group.objects.get_or_create(name="Logistics")
    viewer_group, _ = Group.objects.get_or_create(name="Viewer")

    # ADMIN: ALL PERMISSIONS
    admin_group.permissions.set(Permission.objects.all())

    # INVENTORY MANAGER PERMISSIONS
    inventory_models = [Product, Stock, PurchaseOrder, DemandForecast]
    inventory_permissions = Permission.objects.filter(
        content_type__in=[ContentType.objects.get_for_model(model) for model in inventory_models]
    )
    manager_group.permissions.set(inventory_permissions)

    # LOGISTICS PERMISSIONS
    logistics_models = [StockTransfer, DropShipment]
    logistics_permissions = Permission.objects.filter(
        content_type__in=[ContentType.objects.get_for_model(model) for model in logistics_models]
    )
    logistics_group.permissions.set(logistics_permissions)

    # VIEWER: READ-ONLY
    viewer_permissions = Permission.objects.filter(codename__startswith="view_")
    viewer_group.permissions.set(viewer_permissions)


# ---------------------------------
# GRN MATCH → STOCK ADD
# ---------------------------------
@receiver(post_save, sender=GoodsReceivedNote)
def add_stock_on_grn_match(sender, instance, **kwargs):
    """
    When a GoodsReceivedNote (GRN) is matched:
    - Add received quantity to stock
    - Mark purchase order as COMPLETED
    - Prevent double-processing
    """

    if instance.matched and not instance.processed:
        po = instance.purchase_order

        if po.status != 'COMPLETED':
            with transaction.atomic():
                stock, _ = Stock.objects.get_or_create(
                    product=po.product,
                    location=DEFAULT_WAREHOUSE,
                    defaults={'quantity': 0}
                )
                stock.quantity += instance.received_quantity
                stock.save()

                po.status = 'COMPLETED'
                po.save()

                # Mark GRN as processed to prevent double-processing
                instance.processed = True
                instance.save()


# ---------------------------------
# SALES INVOICE → STOCK DEDUCTION
# ---------------------------------
# GRN MATCH → STOCK ADD
@receiver(post_save, sender=GoodsReceivedNote)
def add_stock_on_grn_match(sender, instance, **kwargs):
    if instance.matched and not instance.processed:
        po = instance.purchase_order
        if po.status != 'COMPLETED':
            with transaction.atomic():
                stock, _ = Stock.objects.get_or_create(
                    product=po.product,
                    location=DEFAULT_WAREHOUSE,
                    defaults={'quantity': 0}
                )
                stock.quantity += instance.received_quantity
                stock.save()

                po.status = 'COMPLETED'
                po.save()

                # Update only processed field to prevent recursion
                GoodsReceivedNote.objects.filter(pk=instance.pk).update(processed=True)


# SALES INVOICE → STOCK DEDUCTION
@receiver(post_save, sender=SalesInvoice)
def reduce_stock_on_invoice(sender, instance, created, **kwargs):
    if created and not instance.processed:
        so = instance.sales_order
        try:
            stock = Stock.objects.get(product=so.product, location=DEFAULT_WAREHOUSE)
        except Stock.DoesNotExist:
            raise ValueError(f"No stock found for product {so.product.name} in {DEFAULT_WAREHOUSE}")

        if stock.quantity < so.quantity:
            raise ValueError(f"Insufficient stock for product {so.product.name}")

        with transaction.atomic():
            stock.quantity -= so.quantity
            stock.save()

            so.status = 'COMPLETED'
            so.save()

            # Update only processed field to prevent recursion
            SalesInvoice.objects.filter(pk=instance.pk).update(processed=True)
