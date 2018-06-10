from django.contrib import admin
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedTabularInline
)
from shop.models import Product, Property, SaleOrder, SaleOrderLine


class PropertyTabularInline(NestedTabularInline):
   model = Property
   extra = 1


class SaleOrderLineTabularInline(NestedTabularInline):
   model = SaleOrderLine
   extra = 1


class SaleOrderAdmin(NestedModelAdmin):
   model = SaleOrder
   inlines = [SaleOrderLineTabularInline, ]


class ProductAdmin(NestedModelAdmin):
   inlines = [PropertyTabularInline,]


admin.site.register(Product, ProductAdmin)
admin.site.register(SaleOrder, SaleOrderAdmin)
