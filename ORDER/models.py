from django.db import models
import uuid
from django.contrib.auth.models import User
from SHOES.models import *

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
     return str(self.user)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    shoe = models.ForeignKey(Shoes,on_delete=models.CASCADE)
    size = models.ForeignKey(SizeShoe,on_delete=models.CASCADE)
    def __str__(self):
     return str(self.cart)
  
  
class Order(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    shoe = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeShoe, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.shoe.name} ({self.size.name})"
    


class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.code
    
    def is_valid(self):
        return self.is_active 




