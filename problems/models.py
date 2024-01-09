from django.db import models
from contests.models import Contest

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    answer = models.CharField(max_length=255)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='problems');

    def __str__(self):
        return self.title

