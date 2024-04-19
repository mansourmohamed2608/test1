from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class PaymentStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    COMPLETED = "completed", _("Completed")
    FAILED = "failed", _("Failed")
    REFUNDED = "refunded", _("Refunded")


class PaymentMethod(models.TextChoices):
    CASH = "cash", _("Cash")
    CREDITS = "credits", _("Credits")


class OrderStatus(models.TextChoices):
    RECEIVED = "received", _("Received")
    PROCESSING = "processing", _("Processing")
    READY_FOR_PACKING = "r for packing", _("Ready for packing")
    READY_FOR_PICK_UP = "r for pickup", _("Ready for pickup")
    DELIVERED = "delivered", _("Delivered")
    WASTE = "waste", _("Waste")
    VOID = "void", _("Void")


class ReturnStatus(models.TextChoices):
    REQUESTED = "requested", _("Requested")
    PROCESSED = "processed", _("Processed")
    COMPLETED = "completed", _("Completed")
    CANCELLED = "cancelled", _("Cancelled")


class OrderType(models.TextChoices):
    DELIVERY = "delivery", _("Delivery")
    DINE_IN = "dine_in", _("Dine In")
    PICKUP = "pickup", _("Pickup")


class OrderSource(models.TextChoices):
    CALL_CENTER = "call center", _("Call Center")
    WEBSITE = "website", _("Website")
    CASHER = "casher", _("casher")
    AGGREGATOR = "aggregator", _("Aggregator")


class DeliveryOptions(models.TextChoices):
    SELF = "self", _("Self")
    PICKUP = "pickup", _("Pickup")
    AGGREGATOR = "aggregator", _("Aggregator")


class AddressType(models.TextChoices):
    HOME = "home", _("Home")
    WORK = "work", _("Work")
    OTHER = "other", _("Other")


class Category(models.Model):
    title = models.CharField(max_length=128)


class Discount(models.Model):
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    description = models.CharField(max_length=128, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.amount}% - {self.description}"


class Address(models.Model):
    type = models.CharField(
        max_length=6, choices=AddressType.choices, default=AddressType.HOME
    )
    country = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=32, null=True, blank=True)


class Customer(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    addresses = models.ManyToManyField(Address)

    def __str__(self) -> str:
        return self.name


class PhoneNumber(models.Model):
    number = models.CharField(max_length=128)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.number


class Aggregator(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.SET_NULL, null=True, related_name="payments"
    )
    method = models.CharField(
        max_length=8,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )
    status = models.CharField(
        max_length=12,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    order_status = models.CharField(
        max_length=15,
        choices=OrderStatus.choices,
        default=OrderStatus.RECEIVED,
    )
    order_type = models.CharField(
        max_length=8,
        choices=OrderType.choices,
        default=OrderType.DELIVERY,
    )
    order_source = models.CharField(
        max_length=12,
        choices=OrderSource.choices,
        default=OrderSource.CALL_CENTER,
    )
    delivery_option = models.CharField(
        max_length=12,
        choices=DeliveryOptions.choices,
        default=DeliveryOptions.SELF,
    )
    payment_method = models.CharField(
        max_length=12,
        choices=PaymentMethod,
        default=PaymentMethod.CASH,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    order_aggregator = models.ForeignKey(
        Aggregator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    delivery_aggregator = models.ForeignKey(
        Aggregator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders_delivered",
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    void_comment = models.ForeignKey(
        "VoidComment", on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    waste_comment = models.ForeignKey(
        "WasteComment", on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )

    discounts = models.ManyToManyField(Discount, blank=True, related_name="orders")
    products = models.ManyToManyField("Product", blank=True, related_name="orders")
    delivered_by = models.CharField(
        max_length=32, blank=True, null=True
    )  # should be a foreignkey

    paid = models.BooleanField(default=False)
    delivery_fees = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
    )
    refund_delivery_charge = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
    )

    placed_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_prep_at = models.DateTimeField(null=True, blank=True)
    finished_prep_at = models.DateTimeField(null=True, blank=True)
    packed_at = models.DateTimeField(null=True, blank=True)
    picked_up_at_time = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def recall(self):
        pass

    def __str__(self) -> str:
        return f"{self.pk}"


class Product(models.Model):
    sku = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    brand = models.ForeignKey(
        "Brand", on_delete=models.SET_NULL, null=True, related_name="brand_products"
    )
    supplier = models.CharField(max_length=128, null=True, blank=True)
    cost_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    retail_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    quantity_in_stock = models.IntegerField(blank=True, null=True)
    reorder_level = models.IntegerField(blank=True, null=True)
    reorder_quantity = models.IntegerField(blank=True, null=True)
    warehouse_location = models.CharField(max_length=128, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    barcode = models.CharField(max_length=128, null=True, blank=True)

    brand = models.ForeignKey(
        "Brand",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="brand_products",
    )
    branch = models.ManyToManyField("Branch", blank=True)


class Invoice(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, related_name="invoices"
    )
    invoice_number = models.CharField(max_length=32, null=True, blank=True)
    billing_details = models.CharField(max_length=128, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(blank=True, null=True)


class Return(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.SET_NULL, null=True, related_name="returns"
    )
    return_reason = models.CharField(max_length=128, null=True, blank=True)
    return_status = models.CharField(
        max_length=12,
        choices=ReturnStatus.choices,
        default=ReturnStatus.REQUESTED,
    )
    refund_amount = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    issued_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    class Range(models.IntegerChoices):
        RATING_1 = 1, "1"
        RATING_2 = 2, "2"
        RATING_3 = 3, "3"
        RATING_4 = 4, "4"
        RATING_5 = 5, "5"

    value = models.IntegerField(
        verbose_name=_("Rating value"),
        choices=Range.choices,
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.TextField(null=True, blank=True)

    customer = models.ForeignKey(
        Customer,
        related_name="reviews",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        related_name="reviews",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.customer} rated {self.order} by {self.value}/5"


class Cluster(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=128)
    location = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    cluster = models.ManyToManyField(Cluster)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=32)
    branches = models.ManyToManyField(Branch)

    def __str__(self):
        return self.name


class VoidComment(models.Model):
    comment = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.comment


class WasteComment(models.Model):
    comment = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.comment
