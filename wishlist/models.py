from django.db import models
from variant.models import Variant
from django.contrib.auth.models import User


# Create your models here.

class Wishlist(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)