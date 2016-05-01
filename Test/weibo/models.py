from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class UserProfiles(models.Model):
    username = models.CharField(max_length=20)
    contents_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    gender = models.CharField(max_length=2)
    intro = models.CharField(max_length=50)
    birthday = models.DateField()

class Contents(models.Model):
    username = models.CharField(max_length=20)
    content = models.TextField(max_length=140)
    comment_count = models.IntegerField(default=0)
    content_time = models.DateTimeField(default=datetime.now())

class Comments(models.Model):
    content_id = models.IntegerField()
    comment_username = models.CharField(max_length=50)
    comment = models.TextField(max_length=100)
    comment_time = models.DateTimeField(default=datetime.now())

class Follows(models.Model):
    username = models.CharField(max_length=20)
    follow_username = models.CharField(max_length=50)

