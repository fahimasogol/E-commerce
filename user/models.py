from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Product
from order.models import Order


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preferences = models.JSONField(blank=True, null=True)  # Store preferences as JSON
    wishlist = models.ManyToManyField(Product, related_name='wishlisted_by')
    shopping_history = models.ManyToManyField(Order, related_name='ordered_by')

    def __str__(self):
        return self.user.username

#  User preferences can vary greatly and may include a diverse range of data types and structures.
#  A JSONField allows you to store this data in a flexible, schema-less format.
# This means you can easily accommodate preferences of different types without needing to alter
# the database schema each time you want to add a new preference type.
