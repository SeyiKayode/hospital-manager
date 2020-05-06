from django.urls import path
from . import views
urlpatterns = [
    path('generate/<int:case_id>/', views.generate, name='generate'),
    path('do_generate/', views.doGenerate, name='do_generate'),
    path('', views.view, name='view_bill'),
    path('pay/', views.pay, name='pay_bill'),
    path('medicines/', views.viewMedicine, name='view_medicine'),
    path('delete/<int:id>/', views.delete, name='delete_bill')
]
