from django.conf.urls import url
from .views import (PlayerListView, PlayerDetailView, TournamentListView,
                    TournamentDetailView, MatchListView, MatchDetailView,
                    RoundListView, RoundDetailView)


urlpatterns = [
    url(r'^players/$', PlayerListView.as_view(), name='player_list'),
    url(r'^players/(?P<pk>[\w-]+)', PlayerDetailView.as_view(), name='player_detail'),
    url(r'tournaments/$', TournamentListView.as_view(), name='tournament_list'),
    url(r'tournaments/(?P<pk>[\w-]+)', TournamentDetailView.as_view(), name='tournament_detail'),
    url(r'matches/$', MatchListView.as_view(), name='match_list'),
    url(r'^matches/(?P<pk>[\w-]+)', MatchDetailView.as_view(), name='match_detail'),
    url(r'rounds/$', RoundListView.as_view(), name='round_list'),
    url(r'rounds/(?P<pk>[\w-]+)', RoundDetailView.as_view(), name='round_detail')
]