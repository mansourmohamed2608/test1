from django.contrib import admin
from .models import (
    Category,
    Discount,
    Address,
    Customer,
    PhoneNumber,
    Aggregator,
    Payment,
    Order,
    Product,
    Invoice,
    Return,
    Review,
    Cluster,
    Branch,
    Brand,
)


# Inline definitions for related models
class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1


# Admin model registrations and customizations
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("amount", "description", "start_date", "end_date", "active")
    list_filter = ("active", "start_date", "end_date")
    search_fields = ("description",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("type", "country", "state", "city", "street", "postal_code")
    list_filter = ("country", "state", "city")
    search_fields = ("street", "postal_code")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")
    inlines = [PhoneNumberInline]


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("number", "customer")
    search_fields = ("number",)


@admin.register(Aggregator)
class AggregatorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "status", "total_amount", "created_at")
    list_filter = ("status", "method")
    search_fields = ("order__id",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_status", "order_type", "customer", "placed_at")
    list_filter = ("order_status", "order_type", "placed_at")
    search_fields = ("customer__name", "id")
    inlines = [PaymentInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "cost_price",
        "retail_price",
        "quantity_in_stock",
    )
    search_fields = ("name", "sku")
    list_filter = ("category",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("order", "invoice_number", "total_amount", "issued_at", "due_at")
    search_fields = ("order__id", "invoice_number")


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "return_reason",
        "return_status",
        "refund_amount",
        "issued_at",
    )
    list_filter = ("return_status",)
    search_fields = ("order__id", "return_reason")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "order", "value", "comment", "created_at")
    list_filter = ("value",)
    search_fields = ("customer__name", "order__id", "comment")


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
