from django.urls import path
from . import views

urlpatterns=[
    path('userprofile',views.userprofile,name='userprofile'),

    path('addaddress/<int:add_id>',views.addaddress,name='addaddress'),
    path('editaddress/<int:edit_id>',views.editaddress,name='editaddress'),
    path('Viewaddress/<int:view_id>',views.Viewaddress,name='Viewaddress'),
    path('deleteaddress/<int:delete_id>',views.deleteaddress,name='deleteaddress'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    # path('orderviewuser/<int:view_ id>',views.orderviewuser,name='orderviewuser'),  
]