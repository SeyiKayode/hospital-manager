from django.urls import path
from . import views
urlpatterns = [
    path('generate/', views.generate, name='generate'),
    path('do_generate/', views.doGenerate, name='do_generate'),
    path('', views.view, name='view_report'),
    path('delete/<int:id>/', views.delete, name='report_delete')
]
