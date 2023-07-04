from rest_framework import serializers
from .models import Question
from accounts.models import Profile


class QuestionSerializer(serializers.ModelSerializer):
    reciever = serializers.ListField(write_only=True)

    class Meta:
        model = Question
        fields = ["question_body", "sender", "reciever", "anonymous"]

    def create(self, validated_data):
        reciever_ids = validated_data.pop("reciever", [])
        question = Question.objects.create(**validated_data)

        receivers = Profile.objects.filter(user__username__in=reciever_ids)
        for receiver in receivers:
            question.reciever.add(receiver)

        return question
