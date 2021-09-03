from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('reserve/', include('reserve.urls')),
    path('admin/', admin.site.urls),
]