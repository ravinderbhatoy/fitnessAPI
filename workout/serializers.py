from rest_framework import serializers
from workout.models import Workout, Exercise, WorkoutExercise
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "name"]  # Only include what you need


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    # Use the serializer above instead of the default ID
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ["id", "sets", "reps", "weight", "exercise"]


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ["id", "date", "exercises"]  # and any other workout fields


# Serializers for creating
class WorkoutCreateSerializer(serializers.ModelSerializer):
    """Create Workout serializer handles POST requests"""

    class Meta:
        model = Workout
        fields = []  # user + date handled internally
