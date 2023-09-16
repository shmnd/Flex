from django.shortcuts import render
from django.contrib import messages




def home(request):
    return render(request,'user/home/index.html')

def blog(request):
    return render(request,'blog/blog.html')