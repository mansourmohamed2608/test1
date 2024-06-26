# Generated by Django 5.0.4 on 2024-04-13 13:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('home', 'Home'), ('work', 'Work'), ('other', 'Other')], default='home', max_length=6)),
                ('country', models.CharField(max_length=128)),
                ('state', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('street', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Aggregator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('description', models.CharField(max_length=128)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('addresses', models.ManyToManyField(to='orders.address')),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('cluster', models.ManyToManyField(to='orders.cluster')),
                ('location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.address')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('labs', models.ManyToManyField(to='orders.lab')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('waste', 'Waste'), ('void', 'Void'), ('completed', 'Completed')], default='pending', max_length=10)),
                ('order_type', models.CharField(choices=[('delivery', 'Delivery'), ('dine_in', 'Dine In'), ('pickup', 'Pickup')], default='delivery', max_length=8)),
                ('order_source', models.CharField(choices=[('call center', 'Call Center'), ('website', 'Website'), ('casher', 'casher'), ('aggregator', 'Aggregator')], default='call center', max_length=12)),
                ('delivery_option', models.CharField(choices=[('call center', 'Call Center'), ('website', 'Website'), ('casher', 'casher'), ('aggregator', 'Aggregator')], default='call center', max_length=12)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('credits', 'Credits')], default='cash', max_length=12)),
                ('void_comment', models.CharField(blank=True, max_length=32, null=True)),
                ('delivered_by', models.CharField(blank=True, max_length=32, null=True)),
                ('delivery_fees', models.DecimalField(decimal_places=2, max_digits=9)),
                ('refund_delivery_charge', models.DecimalField(decimal_places=2, max_digits=9)),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('cooked_at', models.DateTimeField(blank=True, null=True)),
                ('packed_at', models.DateTimeField(blank=True, null=True)),
                ('pickup_time', models.DateTimeField(blank=True, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='orders.category')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.customer')),
                ('delivery_aggregator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_delivered', to='orders.aggregator')),
                ('discounts', models.ManyToManyField(blank=True, related_name='orders', to='orders.discount')),
                ('order_aggregator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.aggregator')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=32, null=True)),
                ('billing_details', models.CharField(blank=True, max_length=128, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('due_at', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('cash', 'Cash'), ('credits', 'Credits')], default='cash', max_length=8)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=12)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='orders.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='orders.payment'),
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=128)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('category', models.CharField(blank=True, max_length=32, null=True)),
                ('supplier', models.CharField(max_length=128)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity_in_stock', models.IntegerField(blank=True, null=True)),
                ('reorder_level', models.IntegerField(blank=True, null=True)),
                ('reorder_quantity', models.IntegerField(blank=True, null=True)),
                ('warehouse_location', models.CharField(blank=True, max_length=128, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('barcode', models.ManyToManyField(to='orders.barcode')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brand_products', to='orders.brand')),
                ('lab', models.ManyToManyField(blank=True, to='orders.lab')),
                ('variant', models.ManyToManyField(to='orders.variant')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='orders', to='orders.product'),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_reason', models.CharField(blank=True, max_length=128, null=True)),
                ('return_status', models.CharField(choices=[('requested', 'Requested'), ('processed', 'Processed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='requested', max_length=12)),
                ('refund_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='returns', to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'poor'), (2, 'fair'), (3, 'good'), (4, 'very good'), (5, 'excellent')], default=0, help_text='1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent', verbose_name='Rating value')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='orders.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='orders.order')),
            ],
        ),
    ]
