from django.db import models
from django.contrib.auth.models import AbstractUser
from twitteruser.models import MyUser
from django.utils import timezone
# Create your models here.


class Tweet(models.Model):
    text = models.CharField(max_length=140)
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE)
    post_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.text
