from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.member_login, name='login'),
    path('logout/', views.member_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('payment/', views.membership_payment, name='payment'),
    path('payment-history/', views.payment_history, name='payment_history'),
]
