"""Askfm App serializers."""

from rest_framework import serializers
from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    """serializer for question"""

    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question", "sender", "anonymous"]

    def to_representation(self, instance):
        """
        Custom representation for the serialized data.
        """
        ins = super().to_representation(instance)
        if ins["anonymous"]:
            ins.pop("sender")
        return ins


class AnswerSerializer(serializers.ModelSerializer):
    """serializer for answer"""

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "question", "answer", "user"]
