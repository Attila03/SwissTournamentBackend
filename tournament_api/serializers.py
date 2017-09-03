from .models import (Player, Tournament, Round, Match, )

from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', 'opponents', 'tournament')


class PlayerDetailFKSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'score')


class PlayerDetailSerializer(serializers.ModelSerializer):

    opponents = PlayerDetailFKSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', 'opponents', 'tournament')


class TournamentListSerializer(serializers.ModelSerializer):

    players = PlayerDetailFKSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'players')


class TournamentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = '__all__'


class MatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'


class MatchDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'


class RoundListSerializer(serializers.ModelSerializer):

    matches = MatchDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Round
        fields = ('id', 'round_num', 'tournament', 'matches')

    def create(self, validated_data):
        matches_data = validated_data.pop('matches')
        round = Round.objects.create(**validated_data)
        for match_data in matches_data:
            Match.objects.create(round=round, **match_data)

        return round


class RoundDetailSerializer(serializers.ModelSerializer):

    matches = MatchDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Round
        fields = ('id', 'round_num', 'tournament', 'matches')







