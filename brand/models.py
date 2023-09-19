from django.db import models

# Create your models here.
class Brand(models.Model):
    names=models.CharField(max_length=50,unique=True)
    date=models.DateField(auto_now=True)
    is_available =  models.BooleanField(default=True)


    def __str__(self) :
        return self.names
    

