from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from players.models import Player, Invitation

# Create your views here.
def main(request):
    try:
        player = Player.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/linkaccounts/')   
    return render(request, 'chat.html', {'player': player})
