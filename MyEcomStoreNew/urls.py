from django.contrib import admin
from django.urls import path, include  # include to import other app urls
from . import views  # assuming you have a views.py in the same directory
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),  # assuming you have a home view
    path('accounts/', include('accounts.urls')),  # your accounts app URLs
    path('shop/', include('shop.urls')),          # your shop app URLs
    path('blog/', include('blog.urls')),          # your blog app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
