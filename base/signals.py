from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import (
    Product,
    Stock,
    StockTransfer,
    PurchaseOrder,
    DropShipment,
    DemandForecast
)

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Automatically creates user groups and assigns permissions
    after migrations are applied.
    """

    # -----------------------------
    # CREATE GROUPS
    # -----------------------------
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    manager_group, _ = Group.objects.get_or_create(name="InventoryManager")
    logistics_group, _ = Group.objects.get_or_create(name="Logistics")
    viewer_group, _ = Group.objects.get_or_create(name="Viewer")

    # -----------------------------
    # ADMIN: ALL PERMISSIONS
    # -----------------------------
    admin_group.permissions.set(Permission.objects.all())

    # -----------------------------
    # INVENTORY MANAGER PERMISSIONS
    # -----------------------------
    inventory_models = [Product, Stock, PurchaseOrder, DemandForecast]
    inventory_permissions = Permission.objects.filter(
        content_type__in=[
            ContentType.objects.get_for_model(model)
            for model in inventory_models
        ]
    )
    manager_group.permissions.set(inventory_permissions)

    # -----------------------------
    # LOGISTICS PERMISSIONS
    # -----------------------------
    logistics_models = [StockTransfer, DropShipment]
    logistics_permissions = Permission.objects.filter(
        content_type__in=[
            ContentType.objects.get_for_model(model)
            for model in logistics_models
        ]
    )
    logistics_group.permissions.set(logistics_permissions)

    # -----------------------------
    # VIEWER: READ-ONLY
    # -----------------------------
    viewer_permissions = Permission.objects.filter(codename__startswith="view_")
    viewer_group.permissions.set(viewer_permissions)
