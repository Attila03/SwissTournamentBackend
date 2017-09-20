from django.conf.urls import url
from .views import (PlayerListView, PlayerDetailView, TournamentListView,
                    TournamentDetailView, MatchListView, MatchDetailView,
                    RoundListView, RoundDetailView, PlayerRegisterListView,
                    TournamentStandingsView, TournamentPairingsView, TournamentRoundView,
                    UserFilteredTournamentView)


urlpatterns = [
    url(r'^players/$', PlayerListView.as_view(), name='player_list'),
    url(r'^players/(?P<pk>[\w-]+)', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^register-players/$', PlayerRegisterListView.as_view(), name='register_player_list'),
    url(r'tournaments/$', TournamentListView.as_view(), name='tournament_list'),
    url(r'tournaments/(?P<pk>[\w-]+)/$', TournamentDetailView.as_view(), name='tournament_detail'),
    url(r'tournaments/(?P<pk>[\w-]+)/get-standings/$', TournamentStandingsView.as_view(), name='get_standings'),
    url(r'tournaments/(?P<pk>[\w-]+)/round/(?P<round_num>[\w-]+)/$', TournamentRoundView.as_view(), name='tournament_round'),
    url(r'tournaments/user/(?P<pk>[\w-]+)', UserFilteredTournamentView.as_view(), name='user_tournaments'),
    url(r'matches/$', MatchListView.as_view(), name='match_list'),
    url(r'^matches/(?P<pk>[\w-]+)', MatchDetailView.as_view(), name='match_detail'),
    url(r'rounds/$', RoundListView.as_view(), name='round_list'),
    url(r'rounds/(?P<pk>[\w-]+)/$', RoundDetailView.as_view(), name='round_detail'),
    url(r'tournaments/(?P<pk>[\w-]+)/get-pairings', TournamentPairingsView.as_view(), name='get_pairings')
]