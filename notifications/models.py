from django.db import models
from twitteruser.models import MyUser
from tweet.models import Tweet


class Notification(models.Model):
    tagged_user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="user_notifciation")
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name="notify_tweet")

    def __str__(self):
        return self.tagged_user.username
