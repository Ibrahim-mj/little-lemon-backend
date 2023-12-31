# Generated by Django 4.2.6 on 2023-10-18 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("menu_items", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("paid", models.BooleanField(default=False)),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=6),
                ),
                ("quantity", models.PositiveIntegerField(default=0)),
                ("delivered", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Orders.cart"
                    ),
                ),
                (
                    "menu_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="menu_items.menuitem",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cart",
            name="items",
            field=models.ManyToManyField(
                related_name="order_item",
                through="Orders.CartItem",
                to="menu_items.menuitem",
            ),
        ),
    ]
