from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserOTP(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()
    


class CustomUser(User):
    emails = models.EmailField(max_length=20, blank=True)

    def __str__(self):
        return self.username


class ReferralCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    used=models.BooleanField(default=False)

    def __str__(self):
        return self.code