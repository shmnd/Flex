from django.contrib import admin
from .models import Product ,Size,price_range,Color

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}


admin.site.register(Product,ProductAdmin)
admin.site.register(Size)
admin.site.register(price_range)
admin.site.register(Color)
