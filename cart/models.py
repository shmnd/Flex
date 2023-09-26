from django.db import models
from django.contrib.auth.models import User
from variant.models import Variant

# Create your models here.
class Cart(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    # product_qty=models.IntegerField(default=1)
    
    # below code quantity come from Varinat or adminside quantity
    # quanty=models.ForeignKey(Variant,on_delete=models.CASCADE)
    single_total=models.BigIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
    
    
    def __str__(self):
        return f"{self.id}"