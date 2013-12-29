from django.db import models

class Faction(models.Model):
    name = models.CharField(max_length=100)
    motto = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
