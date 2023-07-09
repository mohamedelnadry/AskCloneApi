""" Core App Serializer. """
from rest_framework import serializers
from .models import Question, QuestionPost
from accounts.models import Profile


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_body = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = self.context["user"]
        sender = Profile.objects.get(user=user)  ### neeed validation here
        validated_data["sender"] = sender
        question = Question.objects.create(**validated_data)

        return question


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QeustionPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    answar = serializers.CharField()

    def create(self, validated_data):
        user = self.context["user"]
        user_profile = Profile.objects.get(user=user)  ### neeed validation here
        question_id = validated_data.pop("question")
        question = Question.objects.get(pk=question_id)
        if not question:
            raise serializers.ValidationError("Question ID doesn't exists")
        validated_data["question"] = question
        validated_data["user"] = user_profile
        question_post = QuestionPost.objects.create(**validated_data)
        return question_post
