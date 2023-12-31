from collections.abc import Iterable
from django.db import models 
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify
from offers.models import Offer
 
# Create your models here.

class category(models.Model):
    categories=models.CharField(max_length=200,unique=True)
    categories_description=models.TextField(max_length=200 )
    slug=models.SlugField(max_length=225,unique=True)
    is_available =  models.BooleanField(default=True)
    offer=models.ForeignKey(Offer, on_delete=models.SET_NULL,null=True)

    def __str__(self) :
        return self.categories
    