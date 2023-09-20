from django.urls import path
from .import views

urlpatterns=[
    path('productvariant/',views.productvariant,name='productvariant'),
    path('addproductvariant/',views.addproductvariant,name='addproductvariant'),
    path('editproductvariant/<int:variant_id>',views.editproductvariant,name='editproductvariant'),
    path('productvariantdelete/<int:variant_id>',views.productvariantdelete,name='productvariantdelete'),
    path('productvariantview/<int:product_id>',views.productvariantview,name='productvariantview'),
    path('searchvariant/',views.searchvariant,name='searchvariant'),

    path('productsize/',views.productsize,name='productsize'),
    path('addsize/',views.addsize,name='addsize'),
    path('deletesize/<int:size_range_id>',views.deletesize,name='deletesize'),

    path('productcolor',views.productcolor,name='productcolor'),
    path('addcolor',views.addcolor,name='addcolor'),
    path('deletecolor/<int:color_name_id>',views.deletecolor,name='deletecolor'),

    path('imageview/<int:img_id>',views.imageview,name='imageview'),
    path('imagelist/<int:variant_id>',views.imagelist,name='imagelist'),
    path('imagedelete/<int:image_id>',views.imagedelete,name='imagedelete'),
]