""" Core App Veiw. """
from rest_framework import generics
from .serializers import QuestionSerializer
from .models import Question


class QuestionVeiw(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question
