from django.db import models


class Quiz(models.Model):
    hint = models.CharField(max_length=100)
    keyword = models.CharField(max_length=10)
