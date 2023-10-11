from django.db import models
from brand.models import Brand
from category.models import category
from django.utils.text import slugify
from django.urls import reverse
from offers.models import Offer

# Create your models here.

# price range
class price_range(models.Model):
    low=models.IntegerField()
    high=models.IntegerField()
    

# variation
class Size(models.Model):
    size_chart=models.CharField(max_length=30)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.size_chart
    


class Color(models.Model):
    color_name=models.CharField(max_length=50)
    color_code = models.CharField(max_length=15)
    is_available =models.BooleanField(default=True)

    def __str__(self):
        return self.color_name

# product 
class Product(models.Model):
    product_name=models.CharField(unique=True,max_length=50)
    product_price=models.IntegerField()
    product_description=models.TextField(max_length=200,default="good shoes")
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=250,unique=True)
    is_available=models.BooleanField(default=True)
    offer=models.ForeignKey(Offer,on_delete=models.SET_NULL,null=True)

    
    def __str__(self):
        return self.product_name

class ProductReview(models.Model):
    RATING_CHOICES=(
        (1,'1 Star'),
        (2,'2 Star'),
        (3,'3 Star'),
        (4,'4 Star'),
        (5,'5 Star'),
    )

    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating=models.PositiveBigIntegerField(choices=RATING_CHOICES)
    review_text=models.TextField()
    name=models.CharField(max_length=50)
    email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
    

    

    
    
    
    
            