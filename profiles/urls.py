from django.urls import path
from . import views
urlpatterns = [
    path('', views.myProfile, name='profile'),
    path('register/', views.register, name='profile_register'),
    path('do_register/', views.doRegister, name='profile_do_register')
]
