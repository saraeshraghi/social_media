from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    tel = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(default=0)
    address = models.TextField(null=True, blank=True)