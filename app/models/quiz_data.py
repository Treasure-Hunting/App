from django.db import models
from . import Quiz


class QuizData(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
