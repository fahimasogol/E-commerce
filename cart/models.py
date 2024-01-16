# cart/models.py

from django.db import models
from django.conf import settings
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Anonymous'}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
# setting a default quantity of 1 for cart items is a design choice that aligns with typical user behavior and
# simplifies both the user experience and the backend logic. If the user doesn’t want the item, it’s more intuitive
# to remove it from the cart rather than adjusting its quantity to zero.
