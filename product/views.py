from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product,Size,Color,price_range
from .models import Product
from category.models import category
from django.db.models import Q
# from variant.models import Varaint

# Create your views here.

def product(request):
    pass
def createproduct(request):
    pass
def editproduct(request):
    pass
def deleteproduct(request):
    pass
def product_view(requet):
    pass
def searchproduct(request):
    pass