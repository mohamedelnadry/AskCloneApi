from django.urls import path
from .views import QuestionVeiw
urlpatterns = [
    path("create", QuestionVeiw.as_view(), name="create_question")
]
