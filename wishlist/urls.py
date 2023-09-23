from django.urls import path
from .import views
urlpatterns = [
    path('wishlist',views.wishlist,name='wishlist'),
    # path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('add_wishlist1',views.add_wishlist1,name='add_wishlist1'),
    path('removewishlist/<int:wish_id>',views.removewishlist,name='removewishlist'),
]
