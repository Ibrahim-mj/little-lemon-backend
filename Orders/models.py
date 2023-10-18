from django.db import models

from menu_items.models import MenuItem
from Users.models import User


class Cart(models.Model):
    """
    A model representing a shopping cart for a user.
    """
    items = models.ManyToManyField(MenuItem, through='CartItem', related_name='order_item')
    owner = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    delivered = models.BooleanField(default=False)

    def calculate_total_price(self):
        """
        Calculate and update the order total price based on the items in the cart.
        """
        self.total_price = sum([item.price for item in self.items.all()])
        self.save()

    def calculate_quantity(self):
        """
        Calculate and update the order quantity based on the items in the cart.
        """
        self.quantity = self.items.all().count()
        self.save()

class CartItem(models.Model):
    """
    A model representing an item in an order.

    Attributes:
        cart (Cart): The cart that the order item belongs to.
        menu_item (MenuItem): The menu item that was ordered.
        quantity (int): The quantity of the menu item that was ordered.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.title} for {self.order_list.owner.username}"

# I am still not clear about the order concepts yet

# class Order(models.Model):
#     """
#     A model representing an order.

#     Attributes:
#         order_list (Cart): The cart that the order item belongs to.
#         menu_item (MenuItem): The menu item that was ordered.
#         quantity (int): The quantity of the menu item that was ordered.
#     """
#     order_list = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.menu_item.title} for {self.order_list.owner.username}"