from dajax.core import Dajax
from deeds.models import Story
from players.models import Player
from factions.models import Faction
from dajaxice.decorators import dajaxice_register
from django.db.models import F
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.utils.timezone import utc
import cgi
from players import utils

@dajaxice_register
def editFaction(request, motto, description):
    dajax = Dajax()

    player = utils.getPlayer(request.user)
    if player.rank > 0:
        faction = player.faction
        faction.motto = motto
        faction.description = description
        faction.save()

    url = '/faction/' + faction.name + '/'
    dajax.redirect(url, delay=0)
    return dajax.json()


@dajaxice_register
def submitStory(request, data):
    dajax = Dajax()
    data = data.replace('\n','<br />')

    author = utils.getPlayer(request.user)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    try:
        if author.most_recent > now - datetime.timedelta(seconds=60):
            dajax.assign('#warnings','innerHTML','<div class="alert alert-danger">You must wait a minute between posting stories.</div>')
            return dajax.json()
    except:
        pass

    author.most_recent = now
    author.save()

    story = Story(
        author=utils.getPlayer(request.user),
        text=data,
        score=1
    )
    story.save()
    story.userUpvotes.add(request.user)

    updated_html = render_to_string('story.html', {'story': story, 'request': request})
    dajax.assign('#addstory', 'innerHTML', updated_html)

    return dajax.json()

@dajaxice_register
def createFaction(request, name, motto, description):
    dajax = Dajax()

    try:
        faction = Faction.objects.get(name=name)
        dajax.assign('#name-warnings','innerHTML','<div class="alert alert-danger">A faction with that name already exists! Please try another.</div>')
        return dajax.json()
    except:
        pass

    if len(name) == 0:
        dajax.assign('#name-warnings','innerHTML','<div class="alert alert-danger">Your faction must have a name!</div>')
        return dajax.json()

    faction = Faction(
        name=name,
        motto=motto,
        description=description
    )
    faction.save()

    founder = utils.getPlayer(request.user)

    try:
        old_faction = founder.faction
        if len(Player.objects.filter(faction=old_faction)) == 1:
            old_faction.delete()
    except Exception, e:
        pass

    founder.rank = 2
    founder.faction = faction
    founder.save()

    dajax.redirect('/factions/', delay=0)
    return dajax.json()

@dajaxice_register
def voteUp(request, data):
    dajax = Dajax()
    story = Story.objects.get(id=data)

    story.userUpvotes.add(request.user)
    if request.user in story.userDownvotes.all():
        story.userDownvotes.remove(request.user)

    story.score = story.userUpvotes.count() - story.userDownvotes.count()
    story.save()

    author = story.author
    if author != utils.getPlayer(request.user):
        author.score = F('score') + 1
        author.save()

    storyid = '#story' + str(data)
    updated_story = Story.objects.get(id=data)
    updated_html = render_to_string('story.html', {'story': updated_story, 'request': request})
    dajax.assign(storyid, 'innerHTML', updated_html)

    return dajax.json()

@dajaxice_register
def voteDown(request, data):
    dajax = Dajax()
    story = Story.objects.get(id=data)

    story.userDownvotes.add(request.user)
    if request.user in story.userUpvotes.all():
        story.userUpvotes.remove(request.user)

    story.score = story.userUpvotes.count() - story.userDownvotes.count()
    story.save()

    author = story.author
    if author.score > 0 and author != utils.getPlayer(request.user):
        author.score = F('score') - 1
        author.save()

    storyid = '#story' + str(data)
    updated_story = Story.objects.get(id=data)
    updated_html = render_to_string('story.html', {'story': updated_story, 'request': request})
    dajax.assign(storyid, 'innerHTML', updated_html)

    return dajax.json()