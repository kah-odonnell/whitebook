from django.conf.urls import patterns, include, url
from players import views as player_views
from deeds import views as deed_views
from factions import views as faction_views
from chat import views as chat_views
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'whitebook.views.home', name='home'),
    # url(r'^whitebook/', include('whitebook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', player_views.index),
    url(r'^login/', player_views.login),
    url(r'^register/', player_views.register),
    url(r'^linkaccounts/', player_views.linkaccounts),
    url(r'^stories/recent/(?P<limit>.*)', deed_views.getRecentStories),
    url(r'^stories/', player_views.index),
    url(r'^players/', player_views.players),
    url(r'^player/(?P<username>.*)/', player_views.player_info),
    url(r'^factions/', faction_views.factions),
    url(r'^createfaction/', faction_views.create_faction),
    url(r'^faction/(?P<faction>.*)/', faction_views.faction_info),
    url(r'^invite/(?P<username>.*)/', faction_views.invite), 
    url(r'^join/(?P<faction>.*)/', faction_views.join), 
    url(r'^promote/(?P<username>.*)/', faction_views.promote), 
    url(r'^demote/(?P<username>.*)/', faction_views.demote), 
    url(r'^kick/(?P<username>.*)/', faction_views.kick), 
    url(r'^chat/', chat_views.main), 
    url(r'^edit/', faction_views.edit),
)

urlpatterns += staticfiles_urlpatterns()
