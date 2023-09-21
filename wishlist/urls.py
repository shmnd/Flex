from django.urls import path
from .import views
urlpatterns = [
    path('wishlist',views.wishlist,name='wishlist'),
    path('addwishlist',views.addwishlist,name='addwishlist'),
    path('removewishlist/<int:wish_id>',views.removewishlist,name='removewishlist'),
]
