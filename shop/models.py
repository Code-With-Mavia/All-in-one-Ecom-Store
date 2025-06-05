from django.db import models
import uuid
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.name

class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processed', 'Processed'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    items = models.JSONField()  # stores cart items as JSON: product ids, qty, price, etc.
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tracking_id = models.CharField(max_length=12, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    payment_date = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.tracking_id} by {self.customer.full_name}"

