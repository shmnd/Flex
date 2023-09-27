from django.db import models

# Create your models here.
from user.models import User
from checkout.models import Order


class Orderreturn(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    options=models.CharField(max_length=100,null=True)
    reason=models.TextField(null=True)
    
    
    
class Order_cancelled(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)    
    options=models.CharField(max_length=100,null=True)
    reason=models.TextField(null=True)
    
    
    
    
    