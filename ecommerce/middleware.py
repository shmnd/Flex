from typing import Any
from django.shortcuts import render


class Custom404Middleware:
    def __init__(self,get_response):
        self.get_response=get_response
        
        
    def __call__(self, request):
        response=self.get_response(request)
        
        if response.status_code==404:
            status1=404
            return render(request,'error/error.html',{'status1':status1},status=404)
        
        
        if response.status_code==500:
            status1=500
            return render(request,'error/error.html',{'status1':status1},status=500)
        
        if response.status_code==502:
            status1=502
            return render(request,'error/error.html',{'status1':status1},status=502)
        
        return response
    
    
