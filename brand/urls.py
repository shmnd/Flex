from django.urls import path
from .import views


urlpatterns = [
    path('',views.brand,name='brand'),
    path('createbrand.',views.createbrand,name='createbrand'),
    path('editbrand/<int:editbrand_id>',views.editbrand,name='editbrand'),
    path('deletebrand/<int:deletebrand_id>',views.deletebrand,name='deletebrand'),
    path('searchbrand',views.searchbrand,name='searchbrand')
]
