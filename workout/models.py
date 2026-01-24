from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    date = models.DateField(auto_now_add=True)

    class Meta:
        # show new workouts first
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscleGroup = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="exercises"
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    sets = models.IntegerField(null=False)
    reps = models.IntegerField(null=False)
    weight = models.FloatField(null=True, blank=True, verbose_name="Weight(Kg)")

    def __str__(self):
        return f"{self.exercise.name} - {self.workout.date}"
