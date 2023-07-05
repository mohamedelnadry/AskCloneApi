from rest_framework import serializers
from .models import Question
from accounts.models import Profile


class QuestionSerializer(serializers.Serializer):
    question_body = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = self.context["user"]
        sender = Profile.objects.get(user=user)
        validated_data["sender"] = sender
        question = Question.objects.create(**validated_data)

        return question
