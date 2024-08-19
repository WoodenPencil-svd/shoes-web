# Generated by Django 5.0.7 on 2024-08-19 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SHOES", "0007_voucher_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="user",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="cart",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="shoe",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="size",
        ),
        migrations.RemoveField(
            model_name="order",
            name="user",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="order",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="shoe",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="size",
        ),
        migrations.DeleteModel(
            name="Voucher",
        ),
        migrations.DeleteModel(
            name="Cart",
        ),
        migrations.DeleteModel(
            name="CartItem",
        ),
        migrations.DeleteModel(
            name="Order",
        ),
        migrations.DeleteModel(
            name="OrderItem",
        ),
    ]