"""Askfm App urls."""
from django.urls import path
from .views import (
    QuestionCreate,
    GeneralQuestionList,
    AnswerCreate,
    AnswerList,
    AnswerRetrieveDeleteUpdate,
    PrivetQuestion,
    PrivetQuestionList,
)

app_name = "askfm"

urlpatterns = [
    path("question", QuestionCreate.as_view(), name="questionn_create"),
    path("privetquestion", PrivetQuestion.as_view(), name="privet_questionn_create"),
    path("questions", GeneralQuestionList.as_view(), name="general_questionn_list"),
    path("privetquestions", PrivetQuestionList.as_view(), name="privet_questionn_list"),
    path("answer", AnswerCreate.as_view(), name="answer_create"),
    path("answers", AnswerList.as_view(), name="answer_list"),
    path(
        "answer/<int:pk>",
        AnswerRetrieveDeleteUpdate.as_view(),
        name="answer_retrieve_delete_update",
    ),
]
