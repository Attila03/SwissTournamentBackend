from django.shortcuts import render
from django.views import View

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import (Player, Tournament, Round, Match, )
from .serializers import (PlayerSerializer, PlayerDetailSerializer, TournamentListSerializer,
                          TournamentDetailSerializer, MatchListSerializer, MatchDetailSerializer,
                          RoundListSerializer, RoundDetailSerializer)


class Home(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'tournament_api/home.html')


class PlayerRegisterListView(generics.ListCreateAPIView):

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerListView(generics.ListCreateAPIView):

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetailView(generics.RetrieveDestroyAPIView):

    queryset = Player.objects.all()
    serializer_class = PlayerDetailSerializer


class TournamentListView(generics.ListCreateAPIView):

    queryset = Tournament.objects.all()
    serializer_class = TournamentListSerializer


class TournamentDetailView(generics.RetrieveUpdateAPIView):

    queryset = Tournament.objects.all()
    serializer_class = TournamentDetailSerializer


class MatchListView(generics.ListCreateAPIView):

    queryset = Match.objects.all()
    serializer_class = MatchListSerializer

    def get_queryset(self):
        """
        Optionally restricts the Matches to given tournament(keyword=tournament)
        filtering against query paramter in the URL
        """

        queryset = Match.objects.all()
        tournament_id = self.request.query_params.get('tournament', None)
        if tournament_id is not None:
            queryset = queryset.filter(round__tournament__id=tournament_id)
            round_num = self.request.query_params.get('round', None)
            if round_num is not None:
                queryset = queryset.filter(round__round_num=round_num)
        return queryset


class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Match.objects.all()
    serializer_class = MatchDetailSerializer


class RoundListView(generics.ListCreateAPIView):

    queryset = Round.objects.all()
    serializer_class = RoundListSerializer


class RoundDetailView(generics.RetrieveDestroyAPIView):

    queryset = Round.objects.all()
    serializer_class = RoundDetailSerializer
