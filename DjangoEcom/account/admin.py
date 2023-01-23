from django.contrib import admin
from .models import Category, Product, Cart,Cart_products,Order_Item,Order
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cart_products)
admin.site.register(Order)
admin.site.register(Order_Item)

