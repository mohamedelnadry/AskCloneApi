"""Askfm App urls."""
from django.urls import path
from .views import (
    QuestionCreate,
    QuestionList,
    AnswerCreate,
    AnswerList,
    AnswerRetrieveDeleteUpdate,
    PrivetQuestion
)

app_name = "askfm"

urlpatterns = [
    path("question", QuestionCreate.as_view(), name="questionn_create"),
    path("privetquestion", PrivetQuestion.as_view(), name="privet_questionn_create"),
    path("questions", QuestionList.as_view(), name="questionn_list"),
    path("answer", AnswerCreate.as_view(), name="answer_create"),
    path("answers", AnswerList.as_view(), name="answer_list"),
    path(
        "answer/<int:pk>",
        AnswerRetrieveDeleteUpdate.as_view(),
        name="answer_retrieve_delete_update",
    ),
]
