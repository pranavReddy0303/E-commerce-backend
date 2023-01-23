from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255,unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title


class Product(models.Model):
    product_tag = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.IntegerField()
    stock_quantity=models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
   
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '{} {}'.format(self.product_tag, self.name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id}'



class Cart_products(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    Total_price=models.IntegerField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.cart_id,self.product_id,}'     


class Order(models.Model):
    user_id = models.ForeignKey(
        User, default=True, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user_id}'
        
class Order_Item(models.Model):
    order_id = models.ForeignKey(
        Order,on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, default=True, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='cart', on_delete=models.CASCADE)
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.order_id}'







        
