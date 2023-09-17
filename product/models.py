from collections.abc import Iterable
from django.db import models
from brand.models import Brand
from category.models import category
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

# price range
class price_range(models.Model):
    low=models.IntegerField()
    high=models.IntegerField()
    

# variation
class Size(models.Model):
    size_range=models.CharField(max_length=30)
    is_available = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.size_range
    


class Color(models.Model):
    color_name=models.CharField(max_length=50)
    is_avilable =models.BooleanField(default=True)

    def __str__(self):
        return self.color_name


# product 
class Product(models.Model):
    product_name=models.CharField(unique=True,max_length=50)
    product_price=models.IntegerField()
    product_description=models.TextField(max_length=200,default="")
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=250,unique=True)
    is_available=models.BooleanField(default=True)
    # quantity(stock)
    stock=models.PositiveIntegerField()
    
    def __str__(self):
        return self.product_name
    

    
    
    
    
            