from django.contrib.admin import AdminSite
from django.contrib.auth.views import LoginView
from django.urls import path

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('login/', self.login_view, name='login'),
        ]
        return custom_urls + urls

    def login_view(self, request, extra_context=None):
        return LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'show_forgot_password': True,
                'show_show_password': True,
            }
        )(request, extra_context)

admin.site = CustomAdminSite()