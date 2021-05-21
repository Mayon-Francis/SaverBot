from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tweet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tweetId = models.CharField(max_length = 50)

    def __str__(self):
        return self.tweetId