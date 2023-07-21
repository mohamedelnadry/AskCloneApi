"""Askfm App models."""

from django.db import models

# Create your models here.
from core.models import BaseModel
from accounts.models import Profile


class Question(BaseModel):
    question = models.CharField(max_length=255)
    sender = models.ForeignKey(
        Profile, related_name="sender_profile", on_delete=models.PROTECT
    )
    anonymous = models.BooleanField()

    class Meta:
        ordering = ["-question"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question


class Answer(BaseModel):
    question = models.ForeignKey(
        Question, related_name="question_answer", on_delete=models.CASCADE
    )
    answer = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)

    class Meta:
        ordering = ["-question"]
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.question.question
