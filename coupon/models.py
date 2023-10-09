from django.db import models

from django.utils import timezone

class Coupon(models.Model):
    coupon_name=models.CharField(max_length=100)
    coupon_code=models.CharField(max_length=100)
    min_price=models.IntegerField()
    coupon_discount_amount=models.PositiveIntegerField()
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=timezone.now)
    is_available=models.BooleanField(default=True)
    
    def __str__(self) :
        return self.coupon_name
    
    def is_coupon_expired(self):
        return timezone.now().date()>=self.end_date