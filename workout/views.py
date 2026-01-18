from django.http import HttpResponse
from .models import Workout, Exercise
from .serializers import WorkoutSerializer, ExerciseSerializer, WorkoutCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def index(request):
    return HttpResponse("Hey this is index page")


class WorkoutList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workouts = Workout.objects.filter(user=request.user).prefetch_related(
            "exercises__exercise"
        )
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)


class WorkoutCreateView(CreateAPIView):
    """
    Create Workouts
    """

    serializer_class = WorkoutCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExerciseList(APIView):
    """
    List all exercises
    """

    def get(self, request, format=None):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
