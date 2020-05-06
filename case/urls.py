from django.urls import path
from . import views
urlpatterns = [
    path('', views.view, name='view'),
    path('generate/', views.generate, name='generate'),
    path('do_generate/', views.doGenerate, name='do_generate'),
    path('close/', views.close, name='close_case'),
    path('delete/', views.delete, name='delete_case')
]
