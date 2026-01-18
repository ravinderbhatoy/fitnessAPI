from django.urls import path
from workout import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workouts/", views.WorkoutList.as_view(), name="workouts"),
    path("workouts/create/", views.WorkoutCreateView.as_view(), name="workouts"),
    path("exercises/", views.ExerciseList.as_view(), name="exercises"),
]
