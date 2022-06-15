from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES = (
    ('B', 'Books'),
    ('C', 'Car'),
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('S', 'Sofa and Dining'),
    ('D', 'Dogs'),
    ('F', 'Fishes'),
    ('H', 'home decor and garden'),
)
STATE_CHOICES = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh ", "Arunachal Pradesh "),
    ("Assam", "Assam"), ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir ", "Jammu and Kashmir "),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
)


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.TextField(max_length=200, default='')
    price = models.FloatField()
    city = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    product_image = models.FileField()
    sale_status = models.CharField(max_length=100,default='sale')

    def __str__(self):
        return str(self.id)


class Buyerdetail(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="buyer")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="seller")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    Product_name = models.CharField(max_length=150, null=True)
    buyer_username = models.CharField(max_length=100)
    buyer_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.BooleanField(null=True, blank=True)
