from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("workout.urls")),
]

urlpatterns += [
    path('api/login/', obtain_auth_token),
    path("api-auth/", include("rest_framework.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
