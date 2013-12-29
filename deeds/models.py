from django.db import models
from django.contrib.auth.models import User
from players.models import Player

class Vote(models.Model):
    voter = models.ForeignKey(User)
    isUpvote = models.BooleanField()

class Story(models.Model):
    author = models.ForeignKey(Player)
    #faction = models.ForeignKey(Faction)
    text = models.CharField(max_length=1000)
    score = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    userUpvotes = models.ManyToManyField(User, related_name="UpUser")
    userDownvotes = models.ManyToManyField(User, related_name="DownUser")

# Create your models here.
