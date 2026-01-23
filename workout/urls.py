from django.urls import path
from workout import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workouts/", views.WorkoutList.as_view(), name="workouts"),
    path("workouts/create/", views.WorkoutCreateView.as_view(), name="createWorkout"),
    path(
        "workouts/delete/<int:workout_id>/",
        views.WorkoutDeleteView.as_view(),
        name="deleteWorkout",
    ),
    path(
        "workouts/<int:workout_id>/add-exercises/",
        views.AddExercisesToWorkoutView.as_view(),
        name="addExercisesToWorkout",
    ),
    path(
        "workout-exercises/<int:pk>/",
        views.WorkoutExerciseUpdateView.as_view(),
        name="updateWorkoutExercise",
    ),
    path("exercises/", views.ExerciseList.as_view(), name="exercises"),
]
