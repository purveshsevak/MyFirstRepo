from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from library import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls', namespace='catalog')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
