from django.contrib import admin
from order.models import Order, OrderItem, Payment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated', 'paid', 'total_cost']
    list_filter = ['paid', 'created', 'updated']
    search_fields = ['user']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'timestamp', 'successful']
    list_filter = ['successful', 'timestamp']
    search_fields = ['order']
