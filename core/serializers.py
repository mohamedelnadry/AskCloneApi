""" Core App Serializer. """
from rest_framework import serializers
from .models import Question, QuestionPost
from accounts.models import Profile


class QuestionSerializer(serializers.Serializer):
    """
    Serializer for the Question model.
    """
    id = serializers.IntegerField(read_only=True)
    question_body = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """
        Create a new question instance.
        """
        user = self.context["user"]
        sender = Profile.objects.get(user=user)
        validated_data["sender"] = sender
        question = Question.objects.create(**validated_data)

        return question


class AnswarSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuestionPost model.
    """
    class Meta:
        model = QuestionPost
        fields = ["id", "answar", "user"]


class ReQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model used to retrieve question with answers.
    """
    answars = AnswarSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question_body", "sender", "anonymous", "answars"]

    def to_representation(self, instance):
        """
        Custom representation for the serialized data.
        """
        ins = super().to_representation(instance)
        if ins["anonymous"]:
            ins.pop("sender")
        return ins


class QuestionListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model used in the QuestionListVeiw.
    """
    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        """
        Custom representation for the serialized data.
        """
        ins = super().to_representation(instance)
        if ins["anonymous"]:
            ins.pop("sender")
        return ins


class QeustionPostSerializer(serializers.Serializer):
    """
    Serializer for the QuestionPost model used in the QuestionPostVeiw.
    """
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    answar = serializers.CharField()

    def create(self, validated_data):
        """
        Create a new question post instance.
        """
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


class QPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuestionPost model used in the ListQuestionPostVeiw,
    Delete, Update, Retreive QuestionPost.
    """
    class Meta:
        model = QuestionPost
        fields = ["id", "question", "answar", "user"]
        read_only_fields = ["question"]

    def to_representation(self, instance):
        """
        Custom representation for the serialized data.
        """
        inst = super().to_representation(instance)
        question_id = inst.pop("question")
        question = Question.objects.get(pk=question_id)
        inst["question"] = {
            "id": question.id,
            "question": question.question_body,
        }
        return inst

    def update(self, instance, validated_data):
        """
        Update an existing question post instance.
        """
        if not instance.user == validated_data["user"]:
            raise serializers.ValidationError("check your token")

        return super().update(instance, validated_data)
