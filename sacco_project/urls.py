from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('reset-password/', views.custom_password_reset, name='custom_password_reset'),
    path('loans/', views.loans, name='loans'),
    path('', views.dashboard, name='dashboard'),
]