from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL yo'naltiruvchilari
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel uchun URL
    path('', include('locations.urls')),  # Locations ilovasi URL'lari
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Statik fayllar uchun URL