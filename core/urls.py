from django.urls import path
from .views import (
    QuestionVeiw,
    QuestionPostVeiw,
    QuestionListVeiw,
    ListQuestionPostVeiw,
    DeReUpQuestionPost
)

urlpatterns = [
    path("create", QuestionVeiw.as_view(), name="create_question"),
    path("questions", QuestionListVeiw.as_view(), name="list_question"),
    path("createpost", QuestionPostVeiw.as_view(), name="create_question_post"),
    path("listquestionpost", ListQuestionPostVeiw.as_view(), name="list_question_post"),
    path(
        "deletequestionpost/<int:pk>",
        DeReUpQuestionPost.as_view(),
        name="delete_question_post",
    ),
    path(
        "retrievequestionpost/<int:pk>",
        DeReUpQuestionPost.as_view(),
        name="retrieve_question_post",
    ),
    path(
        "updatequestionpost/<int:pk>",
        DeReUpQuestionPost.as_view(),
        name="update_question_post",
    ),
]
