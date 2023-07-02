""" Core App Model. """

from django.db import models
from accounts.models import Profile
from django.core.exceptions import ValidationError


class Question(models.Model):
    question_body = models.CharField(max_length=100)

    sender = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
        )

    reciever = models.ManyToManyField(Profile, related_name="reciever_user")

    anonymous = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question_body


class QuestionPost(models.Model):
    question = models.ForeignKey(
        Question, related_name="questions", on_delete=models.CASCADE
    )
    answar = models.CharField(max_length=255)

    user = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        """
        Before saving, ensure that the user providing the answer is
        included in the list of receivers for the question.
        """
        if self.user not in self.question.reciever.all():
            raise ValidationError(
                "The user is not a receiver of this question"
                )

        super(self).save(*args, **kwargs)

    class Meta:
        verbose_name = "QuestionPost"
        verbose_name_plural = "QuestionsPost"

    def __str__(self):
        return self.question.question_body
