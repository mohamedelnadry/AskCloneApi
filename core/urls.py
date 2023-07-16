from django.urls import path
from .views import (
    QuestionVeiw,
    QuestionPostVeiw,
    QuestionListVeiw,
    ListQuestionPostVeiw,
    DeQuestionPost,
    RQuestionVeiw,
)

urlpatterns = [
    path(
        "create", QuestionVeiw.as_view(), name="create_question"
    ),  # API endpoint to create a new question
    path(
        "questions", QuestionListVeiw.as_view(), name="list_question"
    ),  # API endpoint to list all questions
    path(
        "createpost", QuestionPostVeiw.as_view(), name="create_question_post"
    ),  # API endpoint to create a new question post
    path(
        "listquestionpost", ListQuestionPostVeiw.as_view(), name="list_question_post"
    ),  # API endpoint to list all question posts
    path(
        "deletequestionpost/<int:pk>",
        DeQuestionPost.as_view(),
        name="delete_question_post",
    ),  # API endpoint to delete a question post
    path(
        "retrievequestionpost/<int:pk>",
        DeQuestionPost.as_view(),
        name="retrieve_question_post",
    ),  # API endpoint to retrieve a question post
    path(
        "updatequestionpost/<int:pk>",
        DeQuestionPost.as_view(),
        name="update_question_post",
    ),  # API endpoint to update a question post
    path(
        "question/<int:pk>", RQuestionVeiw.as_view(), name="questions"
    ),  # API endpoint to retrieve a question with answers
]
