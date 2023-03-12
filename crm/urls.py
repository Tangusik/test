from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('crm/', include('trainers.urls')),
    path('admin/', admin.site.urls),
]
