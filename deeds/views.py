from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from players.models import Player
from deeds.models import Story
import datetime
from django.utils.timezone import utc

def getRecentStories(request, limit=10):
    player = Player.objects.get(user=request.user)
    print limit
    newlimit = int(limit) + 10
    stories = list(Story.objects.order_by('-datetime')[0:newlimit])
    if len(stories) <= newlimit:
        hasMore = False
    else:
        hasMore = True
    return render(request, 'stories.html', {
        'player': player,
        'stories': stories,
        'limit': newlimit,
        'filter': 'recent',
        'hasMore': hasMore
    });
