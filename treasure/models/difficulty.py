from django.db import models
from . import Goal, Quiz


class Difficulty(models.Model):
    name = models.CharField(max_length=6)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    quizzes = models.ManyToManyField(Quiz)
