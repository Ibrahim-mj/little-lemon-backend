from django.db import models

class Category(models.Model):
    slug = models.SlugField(unique=True)
    title =  models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self) -> str:
        return self.title


class Cart(models.Model):
    items = models.ManyToManyField(MenuItem, through='OrderItem', related_name='order_item')
    owner = models.ForeignKey('auth.User', related_name='cart', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    delivered = models.BooleanField(default=False)

    def calculate_total_price(self):
        """
        Calculate and update the order total price
        """
        self.total_price = sum([item.price for item in self.items.all()])
        self.save()

    def calculate_quantity(self):
        """
        Calculate and update the order quantity
        """
        self.quantity = self.items.all().count()
        self.save()

class OrderItem(models.Model):
    order_list = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.title} for {self.order_list.owner.username}"