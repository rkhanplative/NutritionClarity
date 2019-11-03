from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
    path('',views.home,name = 'myapp-home'),
    path('upload/',views.upload,name = 'myapp-upload'),
    path('information/',views.information,name = 'myapp-information'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
