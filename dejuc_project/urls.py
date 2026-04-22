"""
URL configuration for dejuc_project — DEJUC INTERNATIONAL GROUP
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin panel
admin.site.site_header = "DEJUC International Group"
admin.site.site_title = "DEJUC Admin"
admin.site.index_title = "Tableau de bord"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
