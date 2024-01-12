from django.db import models
from django.contrib.auth.models import User
from contests.models import Contest, Problem

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rating = models.IntegerField(default=100)

class UserContest(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='participated_contests')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    solved_problems = models.ManyToManyField(Problem, blank=True)
    rated_score = models.IntegerField(default=0)
    unrated_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.contest.title}"


