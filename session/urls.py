from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'session'

urlpatterns = [
    path('', views.index, name='index'),
    # Respiratory Graph
    path('rg/', views.rg_record, name='rg-record'),
    path('rg/<str:username>', views.rg_inquiry, name='rg-inquiry'),
    path('rg/delete/<int:id>', views.rg_delete, name='rg-delete'),
    # Sustained Attention
    # path('sa/', views.rg_record, name='sa-record'),
    # path('sa/<str:username>', views.rg_inquiry, name='sa-inquiry'),
    # path('sa/delete/<int:id>', views.rg_delete, name='sa-delete'),
]