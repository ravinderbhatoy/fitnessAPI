from django.http import HttpResponse
from .models import Workout, Exercise
from .serializers import WorkoutSerializer, ExerciseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
def index(request):
    return HttpResponse("Hey this is index page")


class WorkoutList(APIView):
    """
    List all workouts.
    """

    def get(self, request, format=None):
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)


class ExerciseList(APIView):
    """
    List all exercises
    """

    def get(self, request, format=None):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
