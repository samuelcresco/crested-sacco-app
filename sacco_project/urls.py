from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('reset-password/', views.custom_password_reset, name='custom_password_reset'),
    path('', views.dashboard, name='dashboard'),  # Root URL maps to dashboard
]