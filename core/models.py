""" Core App Model. """

from django.db import models
from accounts.models import Profile


class Question(models.Model):
    """
    Model representing a question.
    """
    question_body = models.CharField(max_length=200)

    sender = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
    )

    anonymous = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question_body


class QuestionPost(models.Model):
    """
    Model representing a question post (answer to a question).
    """
    question = models.ForeignKey(
        Question, related_name="answars", on_delete=models.CASCADE
    )
    answar = models.CharField(max_length=255)

    user = models.ForeignKey(Profile, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "QuestionPost"
        verbose_name_plural = "QuestionsPost"

    def __str__(self):
        return self.question.question_body
