from rest_framework import serializers
from workout.models import Workout, Exercise, WorkoutExercise
from django.contrib.auth.models import User
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "name"]  # Only include what we need


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    # Use the serializer above instead of the default ID
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ["id", "sets", "reps", "weight", "exercise"]


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Workout
        fields = ["id", "user", "date", "exercises"]  # and any other workout fields


# ------------------- Serializers for creating -----------------------------
class WorkoutExerciseCreateSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField()
    sets = serializers.IntegerField()
    reps = serializers.IntegerField()
    weight = serializers.FloatField(required=False)


class WorkoutExerciseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ["sets", "reps", "weight"]

    def validate_sets(self, value):
        if value <= 0:
            raise serializers.ValidationError("Sets must be greater than 0")
        return value

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("At least one field is required")
        return data


class WorkoutCreateSerializer(serializers.Serializer):
    exercises = WorkoutExerciseCreateSerializer(many=True, required=False)

    def create(self, validated_data):
        user = self.context["request"].user
        exercises_data = validated_data.get("exercises", [])

        with transaction.atomic():
            workout = Workout.objects.create(user=user)
            workout_exercises = []

            for item in exercises_data:
                exercise = Exercise.objects.get(id=item["exercise_id"])

                workout_exercises.append(
                    WorkoutExercise(
                        workout=workout,
                        exercise=exercise,
                        date=workout.date,
                        sets=item["sets"],
                        reps=item["sets"],
                        weight=item.get("sets"),
                    )
                )
            WorkoutExercise.objects.bulk_create(workout_exercises)

        return workout
