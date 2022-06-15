from django.contrib import admin
from .models import Product
from .models import Buyerdetail


# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'category', 'description', 'price', \
                    'city', 'state',
                    'product_image']


@admin.register(Buyerdetail)
class BuyerdetailsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'Product_name', 'buyer_username', 'buyer_price', 'quantity']
