""" Core App Veiw. """
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import (
    QuestionSerializer,
    QeustionPostSerializer,
    QuestionListSerializer,
    QPostSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import Question, QuestionPost
from accounts.models import Profile


class QuestionVeiw(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

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


class QuestionListVeiw(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all()


# class DeleteQuestionVeiw(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = QuestionListSerializer
#     queryset = Question.objects.all()


class QuestionPostVeiw(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QeustionPostSerializer
    queryset = QuestionPost.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})

        return context


class ListQuestionPostVeiw(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QPostSerializer
    queryset = QuestionPost.objects.all()

    def get(self, request, *args, **kwargs):
        listquestion = super().get(request, *args, **kwargs)
        if listquestion.data == []:
            return Response(
                {"message": "No Posts added"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return listquestion


class DeReUpQuestionPost(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QPostSerializer
    queryset = QuestionPost.objects.all()

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Question Post Deleted Successfully"},
            status=status.HTTP_200_OK,
        )

    
