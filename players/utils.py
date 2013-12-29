from django.contrib.auth.models import User
from players.models import Player

def userAlreadyExists(username):
    try:
        User.objects.filter(username=username).get()
        return True
    except:
        return False

def minecraftAccountAlreadyExists(mc_username):
    try:
        Player.objects.get(mc_username=mc_username)
        return True
    except:
        return False

def isLinked(user):
    try:
        Player.objects.get(user=user)
        return True
    except:
        return False

def getPlayer(user):
    try:
        x = Player.objects.get(user=user)
        return x
    except:
        return None