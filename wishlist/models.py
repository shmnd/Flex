from django.db import models
from variant.models import Variant

# Create your models here.

class Wishlist(models.Model):
    varinat=models.ForeignKey(Variant,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)