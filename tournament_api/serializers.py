from .models import (Player, Tournament, Round, Match, )

from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', 'opponents', 'tournament')


class PlayerFKSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'score')


class PlayerDetailSerializer(serializers.ModelSerializer):

    opponents = PlayerFKSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', 'opponents', 'tournament')


class TournamentListSerializer(serializers.ModelSerializer):

    players = PlayerFKSerializer(many=True)
    last_concluded_round = serializers.SerializerMethodField()
    total_rounds = serializers.SerializerMethodField()

    def get_last_concluded_round(self, obj):
        return obj.get_last_concluded_round()

    def get_total_rounds(self, obj):
        return obj.get_total_rounds()

    def create(self, validated_data):
        players_data = validated_data.pop('players')
        tournament = Tournament.objects.create(**validated_data, organizer=self.context["request"].user)
        for player_data in players_data:
            Player.objects.create(name=player_data['name'], tournament=tournament)
        return tournament

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'players', 'last_concluded_round', 'total_rounds', 'organizer')


class TournamentDetailSerializer(serializers.ModelSerializer):

    last_concluded_round = serializers.SerializerMethodField()
    total_rounds = serializers.SerializerMethodField()

    def get_last_concluded_round(self, obj):
        return obj.get_last_concluded_round()

    def get_total_rounds(self, obj):
        return obj.get_total_rounds()

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'players', 'last_concluded_round', 'total_rounds')


class MatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'


class MatchPlayerFKSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'name')


class MatchDetailSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    white_player = MatchPlayerFKSerializer()
    black_player = MatchPlayerFKSerializer()

    class Meta:
        model = Match
        fields = '__all__'


class MatchPOSTSerializer(serializers.ModelSerializer):

    white_player = MatchPlayerFKSerializer()
    black_player = MatchPlayerFKSerializer()

    class Meta:
        model = Match
        fields = '__all__'


class RoundListSerializer(serializers.ModelSerializer):

    matches = MatchPOSTSerializer(many=True, read_only=False)

    class Meta:
        model = Round
        fields = ('id', 'round_num', 'tournament', 'concluded', 'matches')

    def create(self, validated_data):
        # import pdb
        # pdb.set_trace()
        matches_data = validated_data.pop('matches')
        round = Round.objects.create(**validated_data)
        for match_data in matches_data:
            white_player_id = match_data.get('white_player').get('id')
            black_player_id = match_data.get('black_player').get('id')
            white_player = Player.objects.get(id=white_player_id)
            black_player = Player.objects.get(id=black_player_id)
            Match.objects.create(round=round, white_player=white_player, black_player=black_player)
        return round


class RoundDetailSerializer(serializers.ModelSerializer):

    matches = MatchDetailSerializer(many=True, read_only=False)
    exists = serializers.BooleanField(default=True)

    class Meta:
        model = Round
        fields = ('id', 'round_num', 'tournament', 'concluded', 'matches', 'exists')
        extra_kwargs = {
            'round_num': {'read_only': True},
            'tournament': {'read_only': True}
        }

    def update(self, instance, validated_data):
        # import pdb
        # pdb.set_trace()
        matches_data = validated_data.pop('matches')
        instance.concluded = validated_data.pop('concluded')
        for match_data in matches_data:
            match_id = match_data.get('id')
            match = Match.objects.get(pk=match_id)
            match.result = match_data.get('result')
            match.save()
        instance.save()
        return instance


class TournamentRoundSerializer(serializers.ModelSerializer):

    pass







