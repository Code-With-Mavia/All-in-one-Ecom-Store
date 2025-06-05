from django.contrib import admin
from .models import Category, Product, Customer, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category']
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'created_at']
    search_fields = ['full_name', 'email']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'customer', 'status', 'payment_status', 'total_price', 'created_at']
    list_filter = ['status', 'payment_status']
    search_fields = ['tracking_id', 'customer__full_name']
