from django.urls import path
from workout import views

urlpatterns = [
    path("", views.index, name="index"),
]
