from django.contrib import admin
from .models import Question, QuestionPost
# Register your models here.

admin.site.register(Question)
admin.site.register(QuestionPost)
