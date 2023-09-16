from collections.abc import Iterable
from django.db import models
from category.models import category
from django.utils.text import slugify

# Create your models here.

class Color(models.Model):
    color_name=models.CharField(max_length=50)
    is_avilable =models.BooleanField(default=True)



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


# product 
class Product(models.Model):
    image1=models.ImageField(upload_to='media/products',default="no images")
    image2=models.ImageField(upload_to='media/products',default="no images")
    image3=models.ImageField(upload_to='media/products',default="no images")
    product_name=models.CharField(unique=True,max_length=50)
    product_price=models.IntegerField()
    sizes=models.ManyToManyField(Size)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    # quantity(stock)
    stock=models.PositiveIntegerField()
    product_description=models.TextField(max_length=200)
    
    
    is_available=models.BooleanField(default=False)
    slug=models.SlugField(max_length=250,unique=True)
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug=slugify(self.product_name)
        super(Product,self).save(*args, **kwargs)
    def __str__(self):
        return self.product_name
    

    
    
    
    
            