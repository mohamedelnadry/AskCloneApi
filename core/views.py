""" Core App Veiw. """
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import QuestionSerializer
from .models import Question


class QuestionVeiw(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Question Created Successfully", "data": response.data},
            status=status.HTTP_201_CREATED,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})

        return context
