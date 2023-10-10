from django.urls import path
from .import views

urlpatterns = [
    path('offer/',views.offer,name='offer'),
    path('addoffer/',views.addoffer,name='addoffer'),
    path('editoffer/<int:offer_id>',views.editoffer,name='editoffer'),
    path('searchoffer/',views.searchoffer,name='searchoffer'),
    path('deleteoffer/<int:delete_id>',views.deleteoffer,name='deleteoffer')
]
