from django.urls import path
from .views import QuestionVeiw, QuestionPostVeiw, QuestionListVeiw

urlpatterns = [
    path("create", QuestionVeiw.as_view(), name="create_question"),
    path("questions", QuestionListVeiw.as_view(), name="list_question"),
    path("createpost", QuestionPostVeiw.as_view(), name="create_question_post"),
]
