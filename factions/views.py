from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from factions.models import Faction
from players.models import Player, Invitation
from deeds.models import Story
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User

def faction_info(request, faction=""):
    player = Player.objects.get(user=request.user)
    faction = Faction.objects.get(name=faction)
    players = list(Player.objects.filter(faction=faction))
    if Invitation.objects.filter(faction=faction, player=player).count() > 0:
        invited = True
    else: 
        invited = False
    return render(request, 'factionInfo.html', {
        'player': player,
        'faction': faction,
        'players': players,
        'invited': invited
    })

def factions(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html', {})
    else:
        player = Player.objects.get(user=request.user)
        factions = list(Faction.objects.all())
        return render(request, 'factions.html', {
            'player': player,
            'factions': factions,
        })

def create_faction(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html', {})
    else:
        player = Player.objects.get(user=request.user)
        if player.faction is not None:
            in_faction = True
        else:
            in_faction = False
        return render(request, 'createfaction.html', {
            'player': player,
            'in_faction': in_faction
        }) 

def invite(request, username=""):
    if not request.user.is_authenticated():
        return render(request, 'login.html', {})
    else:
        player = Player.objects.get(user=request.user)
        other_player = Player.objects.get(mc_username=username)
        url = '/player/' + username + '/'
        if player.rank > 0:
            invite = Invitation(faction=player.faction, player=other_player)
            invite.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)

def join(request, faction=""):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    url = '/faction/' + faction + '/'
    player = Player.objects.get(user=request.user)
    faction = Faction.objects.get(name=faction)
    invites = Invitation.objects.filter(player=player, faction=faction)
    if len(invites) > 0:
        player.faction = faction
        player.rank = 0
        player.save()
        for invite in invites:
            invite.delete()
    return HttpResponseRedirect(url)

def promote(request, username=""):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    url = '/player/' + username + '/'
    player = Player.objects.get(user=request.user)
    other_player = Player.objects.get(mc_username=username)
    if (other_player.faction == player.faction) and (player.rank > other_player.rank):
        other_player.rank = 1
        other_player.save()
        return HttpResponseRedirect(url)

def kick(request, username=""):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    url = '/player/' + username + '/'
    player = Player.objects.get(user=request.user)
    other_player = Player.objects.get(mc_username=username)
    if (other_player.faction == player.faction) and (player.rank > other_player.rank):
        other_player.faction = None
        other_player.rank = 0
        other_player.save()
        return HttpResponseRedirect(url)

def demote(request, username=""):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    url = '/player/' + username + '/'
    player = Player.objects.get(user=request.user)
    other_player = Player.objects.get(mc_username=username)
    if (other_player.faction == player.faction) and (other_player.rank == 1) and (player.rank > other_player.rank):
        other_player.rank = 0
        other_player.save()
        return HttpResponseRedirect(url)
