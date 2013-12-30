# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from players.models import Player, Invitation
from deeds.models import Story
import datetime
from django.utils.timezone import utc
import utils
import minecraft

def index(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'login.html', {})
        else:
            try:
                player = Player.objects.get(user=request.user)
            except:
                return HttpResponseRedirect('/linkaccounts/')               
            stories = list(Story.objects.order_by('-datetime')[0:10])
            return render(request, 'stories.html', {
                'player': player,
                'stories': stories,
                'limit': 10,
                'filter': 'recent',
                'hasMore': True
            })

def login(request):
    if request.method == 'GET':
        logout(request)
        return render(request, 'login.html', {})
    if request.method == 'POST':
        try:
            username = request.POST['InputUsername']
            password = request.POST['InputPassword']
        except:
            return render(request, 'login.html', {
                'error': True,
                'errormsg': 'Invalid username or password. Please try again.'
            })
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            if not utils.isLinked(user):
                return HttpResponseRedirect('/linkaccounts/')
            else:
                return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {
                'error': True,
                'errormsg': 'Invalid username or password. Please try again.'
            })

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['InputUsername']
            password = request.POST['InputPassword']
            confirmpw = request.POST['InputConfirmPw']
        except:
            return render(request, 'register.html', {
                'error': True,
                'errormsg': 'Something went wrong. Please try again.'
            })            
        if password != confirmpw:
            return render(request, 'register.html', {
                'error': True,
                'errormsg': 'Those passwords do not match! Please try again.'
            })
        elif utils.userAlreadyExists(username):
            return render(request, 'register.html', {
                'error': True,
                'errormsg': 'This username has already been registered! Please use another.'
            })
        else:
            User.objects.create_user(username, "No email", password)
            auth_login(request, authenticate(username=username, password=password))
            return HttpResponseRedirect('/linkaccounts/')
    if request.method == 'GET':
        return render(request, 'register.html', {})

def linkaccounts(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        username = request.POST['MCUsername']
        password = request.POST['MCPassword']
        verified = minecraft.connect_minecraft(username, password)
        if verified is False:
            return render(request, 'linkaccounts.html', {
                'error': True,
                'errormsg': 'minecraft.net does not recognize your login credentials. Please try again'
            })
        else:
            if utils.minecraftAccountAlreadyExists(verified):
                return render(request, 'linkaccounts.html', {
                    'error': True,
                    'errormsg': 'Your minecraft account has already been registered on The White Book. Please use another.'
                })
            else: 
                now = datetime.datetime.utcnow().replace(tzinfo=utc)               
                player = Player(user=request.user, mc_username=verified, score=0, rank=0, most_recent=(now - datetime.timedelta(seconds=60)))
                player.save()
                return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'linkaccounts.html', {})

def players(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'login.html', {})
        else:
            player = Player.objects.get(user=request.user)
            players = list(Player.objects.all().order_by('-score'))
            return render(request, 'players.html', {
                'player': player,
                'players': players,
            })

def player_info(request, username=""):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'login.html', {})
        else:
            player = Player.objects.get(user=request.user)
            other_player = Player.objects.get(mc_username=username)
            stories = Story.objects.filter(author=other_player).order_by('-score')
            if Invitation.objects.filter(faction=player.faction, player=other_player).count() > 0:
                invited = True
            else: 
                invited = False
            return render(request, 'player_info.html', {
                'player': player,
                'other_player': other_player,
                'stories': stories,
                'invited': invited
            })
