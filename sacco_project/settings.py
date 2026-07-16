"""
Django settings for sacco_project project.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://web-production-63626.up.railway.app']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sacco_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sacco_project.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# CUSTOM SETTINGS
# ============================================

# Login & Logout Redirects
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Admin Panel Branding
ADMIN_SITE_HEADER = "Crested SS 2005 Class - Banking System"
ADMIN_SITE_TITLE = "Crested SS 2005 Class"

# Session Settings - Stay logged in for 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds

# Password Reset (prints link to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
PASSWORD_RESET_TIMEOUT = 14400  # 4 hours
📁 Complete core/templates/admin/base_site.html
File Location: C:\Users\SAM\Desktop\sacco-app\core\templates\admin\base_site.html

html
{% extends "admin/base_site.html" %}

{% block extrahead %}
{{ block.super }}
<style>
    .theme-toggle { display: none !important; }
    #header .theme-toggle { display: none !important; }
    .theme-toggle-wrapper { display: none !important; }
    #header { background: linear-gradient(135deg, #0d1b2a, #1a3a5c) !important; padding: 15px 30px !important; }
    #header h1 { color: white !important; font-size: 22px !important; font-weight: 600 !important; }
    .forgot-password-container { text-align: center; margin-top: 15px; padding-top: 10px; border-top: 1px solid #e9ecef; }
    .forgot-password-container a { color: #1a3a5c; text-decoration: none; font-weight: 500; }
    .forgot-password-container a:hover { text-decoration: underline; }
    .show-password-container { text-align: left; margin-top: 8px; }
    .show-password-container input[type="checkbox"] { width: auto !important; margin-right: 5px !important; display: inline-block !important; }
    .show-password-container label { font-size: 14px; color: #555; cursor: pointer; }
</style>
{% endblock %}

{% block content %}
{{ block.super }}

<!-- FORGOT PASSWORD LINK -->
<div class="forgot-password-container">
    <a href="/accounts/password_reset/">🔑 Forgot Password?</a>
</div>

<!-- SHOW PASSWORD TOGGLE -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    var pwd = document.getElementById('id_password');
    if (pwd) {
        var container = document.createElement('div');
        container.className = 'show-password-container';
        var chk = document.createElement('input');
        chk.type = 'checkbox';
        chk.id = 'show-pwd';
        var lbl = document.createElement('label');
        lbl.htmlFor = 'show-pwd';
        lbl.textContent = '👁️ Show Password';
        container.appendChild(chk);
        container.appendChild(lbl);
        pwd.parentNode.insertBefore(container, pwd.nextSibling);
        chk.addEventListener('change', function() {
            pwd.type = this.checked ? 'text' : 'password';
        });
    }
});
</script>
{% endblock %}s