from django.db import models
from django.contrib.auth.models import User
from factions.models import Faction

class Player(models.Model):
    user = models.OneToOneField(User)
    faction = models.ForeignKey(Faction, null=True, default=None)
    rank = models.PositiveIntegerField()
    mc_username = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    most_recent = models.DateTimeField()

class Invitation(models.Model):
    faction = models.ForeignKey(Faction)
    player = models.ForeignKey(Player)
# Create your models here.
