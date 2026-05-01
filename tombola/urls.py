from django.urls import path
from . import views

app_name = 'tombola'

urlpatterns = [
    path('', views.tombola_list, name='list'),
    path('<slug:slug>/', views.tombola_detail, name='detail'),
    path('<slug:slug>/buy/', views.tombola_buy_ticket, name='buy_ticket'),
    path('<slug:slug>/winners/', views.tombola_winners, name='winners'),
    path('<slug:slug>/draw/', views.tombola_draw, name='draw'),
]
