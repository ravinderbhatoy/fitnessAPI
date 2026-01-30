from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Workout, Exercise, WorkoutExercise
from .serializers import (
    WorkoutSerializer,
    ExerciseSerializer,
    WorkoutCreateSerializer,
    WorkoutExerciseUpdateSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound, PermissionDenied

# Create your views here.


def index(request):
    return HttpResponse("Hey this is index page")


class WorkoutList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # workouts = Workout.objects.filter(user=request.user).prefetch_related(
        #     "exercises__exercise"
        # )
        workouts = Workout.objects.filter(user=User.objects.first()).prefetch_related(
            "exercises__exercise"
        )
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)


class WorkoutDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            workout = Workout.objects.prefetch_related(
                "exercises__exercise").get(pk=pk, user=User.objects.first())  # change to request.user
        except Workout.DoesNotExist:
            raise NotFound("Workout not found")
        serializer = WorkoutSerializer(workout)
        return Response(serializer.data)


class WorkoutCreateView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WorkoutCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        workout = serializer.save()
        return Response(WorkoutSerializer(workout).data, status=201)


class WorkoutDeleteView(APIView):
    def delete(self, request, workout_id):
        workout = get_object_or_404(Workout, id=workout_id)
        workout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddExercisesToWorkoutView(APIView):
    """
    Add new exercises to workout
    """

    def post(self, request, workout_id):
        workout = get_object_or_404(Workout, id=workout_id)
        exercises_data = request.data.get("exercises")

        if not exercises_data:
            return Response({"error": "exercises list is required"}, status=400)

        objs = []
        for item in exercises_data:
            exercise = get_object_or_404(Exercise, id=item["exercise_id"])
            objs.append(
                WorkoutExercise(
                    workout=workout,
                    exercise=exercise,
                    date=workout.date,
                    sets=item["sets"],
                    reps=item["reps"],
                    weight=item.get("weight"),
                )
            )
        WorkoutExercise.objects.bulk_create(objs)

        return Response(
            {"message": "Exercises added successfully"}, status=status.HTTP_201_CREATED
        )


class WorkoutExerciseDetailView(APIView):

    def get_object(self, pk, user):
        try:
            obj = WorkoutExercise.objects.select_related("workout").get(pk=pk)
        except WorkoutExercise.DoesNotExist:
            raise NotFound("Workout exercise not found")

        if user != obj.workout.user:
            raise PermissionDenied("You do not own this workout")

        return obj

    def patch(self, request, pk):
        request.user = User.objects.first()  # for testing
        workout_exercise = self.get_object(pk, request.user)
        serializer = WorkoutExerciseUpdateSerializer(
            workout_exercise, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # fetch object
        request.user = User.objects.first()  # for testing
        workout_exercise = self.get_object(pk, request.user)
        workout_exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExerciseList(APIView):
    """
    List all exercises
    """

    def get(self, request, format=None):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)


class ExerciseProgressView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, exercise_id):
        data = (
            WorkoutExercise.objects.filter(
                exercise_id=exercise_id,
            )
            .order_by("date")
            .values("date", "exercise__name", "sets", "reps", "weight")
        )
        return Response(list(data))


class ExercisePRView(APIView):
    def get(self, request, exercise_id):
        qs = WorkoutExercise.objects.filter(
            workout__user=User.objects.first(),  # change to login user
            exercise_id=exercise_id,
            weight__isnull=False,
        )
        pr = qs.aggregate(max_weight=Max("weight"))["max_weight"]
        exercise = get_object_or_404(Exercise, id=exercise_id)
        return Response({"exercise": exercise.name, "pr": pr})
