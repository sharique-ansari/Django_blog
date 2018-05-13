from django.db import models
from django.utils import timezone


class Word(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    word_title = models.CharField(max_length=200)
    meaning = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.word_title

# Create your models here.
