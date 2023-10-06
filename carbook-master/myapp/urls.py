from django.urls import path,include
from . import views 

urlpatterns = [
    path('',views.index,name='index'),
    path('seller_index',views.seller_index,name="seller_index"),
    path('about',views.about,name='about'),
    path('services',views.services,name='services'),
    path('car',views.car,name='car'),
    path('contact',views.contact,name='contact'),
    path('signup',views.signup,name='signup'),
    path('ajax/e_verify/',views.e_verify,name='e_verify'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('fpswd',views.fpswd,name='fpswd'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('set_pswd',views.set_pswd,name='set_pswd'),
    path('our_services',views.our_services,name='our_services'),
    path('cars',views.cars,name='cars'),
    path('add_car',views.add_car,name='add_car'),
    path('update_car/<int:pk>',views.update_car,name='update_car'),
    path('delete_car/<int:pk>',views.delete_car,name='delete_car'),
    path('car_details/<int:pk>',views.car_details,name='car_details'),
    path('inquiry/<int:pk>',views.inquiry,name='inquiry'),
    path('view_inq',views.view_inq,name='view_inq'),
    path('c_details/<int:pk>',views.c_details,name='c_details'),


]
