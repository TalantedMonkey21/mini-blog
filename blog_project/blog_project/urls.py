from django.contrib import admin
from django.urls import path, include
from blog.views import healthz

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz/', healthz),
    path('', include('blog.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
]