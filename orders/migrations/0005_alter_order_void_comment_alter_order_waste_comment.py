# Generated by Django 5.0.4 on 2024-04-14 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_delivery_fees_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='void_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.voidcomment'),
        ),
        migrations.AlterField(
            model_name='order',
            name='waste_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.wastecomment'),
        ),
    ]