from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'ADMIN'),
        ('customer', 'CUSTOMER'),
        ('delivery_partner', 'DELIVERY'),
    )
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    role=models.CharField(max_length=20, choices=ROLE_CHOICES)
    
class Resturant(models.Model):
    name=models.CharField(max_length=100)
    role=models.CharField(max_length=100)

class FoodItem(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    restaurant=models.ForeignKey(Resturant, on_delete=models.CASCADE)
    
class Order(models.Model):
    STATUS=(
        ('placed', 'PLACED'),
        ('preparing', 'PREPARING'),
        ('out_of_delivery', 'OUT_OF_DELIVERY'),
        ('delivered', 'DELIVERED'),
    )
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_partner=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery')
    items=models.ManyToManyField(FoodItem)
    status=models.CharField(max_length=20, choices=STATUS, default='placed')