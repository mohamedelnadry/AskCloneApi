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


class PrivetQuestion(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        sender = ProfileService.get_profile(self.request.user)
        reciever = request.data.pop("reciever")
        user = PrivetQuestion.reciever_check(reciever)
        if user == None or sender == None:
            return Response(
                {"detail": "User Doesn't Exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data["question"]
            privet_question = PrivetQuestion.create_privet_question(
                sender, user, question
            )
            if privet_question:
                return Response(
                    {"detail": "Question Created Successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"detail": "Error in Create Privet Question"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def reciever_check(reciever):
        if not isinstance(reciever, int):
            return None
        profile = Profile.objects.get(pk=reciever)
        if profile:
            return profile
        return None

    @staticmethod
    def create_privet_question(sender, user, question):
        try:
            privetquestion = Question.objects.create(question=question, sender=sender)
            privetquestion.privet = True
            privetquestion.save()
            answer = Answer.objects.create(question=privetquestion, user=user)
            answer.privet = True
            answer.save()
            return Question
        except:
            return None


class QuestionList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = ProfileService.get_profile(self.request.user)
        if not user:
            return Response(
                {"detail": "User Doesn't Exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = AnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        question = serializer.validated_data["question"]
        answer = serializer.validated_data["answer"]
        answer_create = AnswerCreate.create_answer(user, question, answer)
        if answer_create:
            return Response(
                {"detail": "Answer Created Successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "User have already answer in this question"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def create_answer(user, question, answer):
        instance, created = Answer.objects.get_or_create(
            user=user, question=question, answer=answer
        )
        if instance.user == user and instance.answer != None:
            return None

        if instance:
            instance.privet = False
            instance.answer = answer
            instance.save()
            return instance

        if created:
            return created


class AnswerList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        user = ProfileService.get_profile(self.request.user)
        answer = Answer.objects.filter(user=user, privet=False)
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

        answer = AnswerRetrieveDeleteUpdate.get_answer_object(id)
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
        answer_update = AnswerRetrieveDeleteUpdate.update_answer(
            answer, question, user, instance
        )
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
        answer = AnswerRetrieveDeleteUpdate.delete_answer(instance, user)
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
