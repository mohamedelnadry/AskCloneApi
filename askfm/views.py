"""Askfm App views."""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.views import APIView
from .models import Question, Answer
from accounts.models import Profile
from .serializers import QuestionSerializer, AnswerSerializer


class ProfileService:
    @staticmethod
    def get_profile(user):
        profile = Profile.objects.get(user=user)
        if not profile:
            return None
        return profile


class QuestionCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        sender = ProfileService.get_profile(self.request.user)
        serializer.save(sender=sender)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            {"detail": "Question Created Successfully"},
            status=status.HTTP_201_CREATED,
        )


class QuestionList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        user = ProfileService.get_profile(self.request.user)
        if not user:
            raise Response(
                {"detail": "User Doesn't Exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            {"detail": "Answer Created Successfully"},
            status=status.HTTP_201_CREATED,
        )


class AnswerList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        user = ProfileService.get_profile(self.request.user)
        answer = Answer.objects.filter(user=user)
        return answer


class AnswerRetrieveDeleteUpdate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @property
    def get_answer(self):
        id = self.kwargs.get("pk", None)
        if id is None:
            return Response(
                {"detail": "Id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        answer = self.get_answer_object(id)
        if answer is None:
            return Response(
                {"detail": "Answer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return answer

    def get(self, request, *args, **kwargs):
        answer = self.get_answer
        serializer = AnswerSerializer(answer)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": serializer.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_answer
        user = ProfileService.get_profile(self.request.user)
        serializer = AnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        answer = serializer.validated_data["answer"]
        question = serializer.validated_data["question"]
        answer_update = self.update_answer(answer, question, user, instance)
        if answer_update is None:
            return Response(
                {"detail": "User or Question not correct "},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Answer Updated Successfully "},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_answer
        user = ProfileService.get_profile(self.request.user)
        answer = self.delete_answer(instance, user)
        if answer is None:
            Response(
                {"detail": "Check user please "},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Answer Deleted Successfully "},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def get_answer_object(id):
        answer = Answer.objects.get(id=id)
        if answer:
            return answer
        return None

    @staticmethod
    def update_answer(answer, question, user, instance):
        if user == instance.user and question == instance.question:
            return Answer.objects.update(answer=answer)
        return None

    @staticmethod
    def delete_answer(instance, user):
        if user == instance.user:
            instance.delete()
            return True
        return None
