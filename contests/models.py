from django.db import models

class Contest(models.Model) :
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    answer = models.CharField(max_length=255)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='problems');

    def __str__(self):
        return self.title

