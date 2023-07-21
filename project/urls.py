"""
URL configuration for project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path("admin/", admin.site.urls),
    # Your stuff: custom urls includes go here
    path("api/v1/", include("askfm.urls", namespace="askfm")),
    path("api/accounts/", include("accounts.urls")),
]
