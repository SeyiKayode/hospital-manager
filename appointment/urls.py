from django.urls import path
from . import views
urlpatterns = [
    path('', views.view, name='view'),
    path('book/', views.book, name='book'),
    path('do_book/', views.doBook, name='do_book'),
    path('change_appointment/<int:id>/', views.changeAppointment, name='change_appointment'),
    path('do_change/', views.doChange, name='do_change_appointment'),
    path('delete/<int:id>/', views.delete, name='delete')
]
