""" Core App Veiw. """
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import (
    QuestionSerializer,
    QeustionPostSerializer,
    QuestionListSerializer,
    QPostSerializer,
    ReQuestionSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import Question, QuestionPost
from accounts.models import Profile


class QuestionVeiw(generics.CreateAPIView):
    """
    API view to create a new question.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to add custom response data.
        """
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Question Created Successfully", "data": response.data},
            status=status.HTTP_201_CREATED,
        )

    def get_serializer_context(self):
        """
        Add the current user to the serializer context.
        """
        context = super().get_serializer_context()
        context.update({"user": self.request.user})

        return context


class RQuestionVeiw(generics.RetrieveAPIView):
    """
    API view to retrieve a question with its associated answers.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ReQuestionSerializer
    queryset = Question.objects.all()

    def get_object(self):
        """
        Get the question with the provided ID and attach its answers.
        """
        pk = self.kwargs.get("pk")
        question = get_object_or_404(Question, id=pk)
        answars = QuestionPost.objects.filter(question=question)
        question.answars.set(answars)
        return question


class QuestionListVeiw(generics.ListAPIView):
    """
    API view to list all questions.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all()


class QuestionPostVeiw(generics.CreateAPIView):
    """
    API view to create a new question post.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QeustionPostSerializer
    queryset = QuestionPost.objects.all()

    def get_serializer_context(self):
        """
        Add the current user to the serializer context.
        """
        context = super().get_serializer_context()
        context.update({"user": self.request.user})

        return context


class ListQuestionPostVeiw(generics.ListAPIView):
    """
    API view to list all question posts.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QPostSerializer
    queryset = QuestionPost.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Override the get method to handle empty response.
        """
        listquestion = super().get(request, *args, **kwargs)
        if listquestion.data == []:
            return Response(
                {"message": "No Posts added"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return listquestion


class DeQuestionPost(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a question post.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QPostSerializer
    queryset = QuestionPost.objects.all()

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to return a success message.
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Question Post Deleted Successfully"},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        """
        Override the update method to handle token validation and return a success message.
        """
        user = self.request.user
        profile = Profile.objects.get(user=user)
        instance = self.get_object()
        request.data["user"] = profile.id
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Question Post Updated Successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
