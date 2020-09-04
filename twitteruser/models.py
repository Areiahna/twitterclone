from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class MyUser(AbstractUser):
    display_name = models.CharField(max_length=40, blank=True, unique=True)
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return f"{self.display_name}"
