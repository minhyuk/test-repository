from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'session'

urlpatterns = [
    path('', views.index, name='index'),
    path('rg/', views.rg_record, name='rg-record'),
    path('rg/<str:username>', views.rg_inquiry, name='rg-inquiry'),
    # path('<str:username>', views.medass_inquiry, name='inquiry'),
    # path('delete/<int:id>', views.medass_delete, name='delete'),
]