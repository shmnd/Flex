from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50,blank=True)
    email=models.EmailField(max_length=59)
    address=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=10,blank=True)
    state=models.CharField(max_length=50,blank=True)
    city=models.CharField(max_length=50,blank=True)
    pincode=models.CharField(max_length=50,blank=True)
    order_note=models.CharField(max_length=100,blank=True,null=True)
    is_available=models.BooleanField(null=True,default=True)
    
    
    def __str__(self):
        return f"{self.user}"
    
class Wallet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    wallet=models.PositiveBigIntegerField(null=True)
    
    def add_to_wallet(user, amount):
        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            # Create a new wallet if it doesn't exist for the user
            wallet = Wallet.objects.create(user=user, wallet=amount)
        else:
            # Update the existing wallet balance
            wallet.wallet += amount
            wallet.save()