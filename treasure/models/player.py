from django.db import models
from . import Difficulty, QuizData


class Player(models.Model):
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    quizzes = models.ManyToManyField(QuizData)
    progress = models.IntegerField(default=0)
