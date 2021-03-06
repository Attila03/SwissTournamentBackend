from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from math import log2, ceil


class Player(models.Model):

    name = models.CharField(max_length=100)
    tournament = models.ForeignKey('Tournament', related_name='players')
    opponents = models.ManyToManyField('Player', blank=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "tournament")


class Tournament(models.Model):

    name = models.CharField(max_length=150,  unique=True)
    organizer = models.ForeignKey(User, default='1')
    # winner = models.ForeignKey('Player', null=True, blank=True, related_name='tournament_won')

    def __str__(self):
        return self.name

    def get_standings(self):
        return self.players.all().order_by('-score')

    def get_last_concluded_round(self):
        if self.round_set.filter(concluded=True):
            return self.round_set.filter(concluded=True).order_by('-round_num').first().round_num
        else:
            return 0

    def get_total_rounds(self):
        player_count = self.players.count()
        if player_count:
            return ceil(log2(player_count))
        else:
            return 0

    def get_pairings(self):
        matched = set()
        current_standings = self.get_standings()
        pairings = []
        unmatched = []
        for i, player1 in enumerate(current_standings):
            if player1 not in matched:
                for player2 in current_standings[i+1:]:
                    if player2 not in player1.opponents.all() and player2 not in matched:
                        pairings.append((player1.id, player2.id))
                        matched.add(player1)
                        matched.add(player2)
                        break
                else:
                    unmatched.append(player1)
        if unmatched:
            for i in range(0,len(unmatched),2):
                pairings.append((unmatched[i].id, unmatched[i+1].id))

        return pairings


class Round(models.Model):

    tournament = models.ForeignKey('Tournament')
    round_num = models.IntegerField()
    concluded = models.BooleanField(default=False)

    class Meta:
        unique_together = ("tournament", "round_num")

    def __str__(self):
        return "{} - Round {} ".format(self.tournament, self.round_num)


class Match(models.Model):

    WHITE = 'white'
    BLACK = 'black'
    DRAW = 'draw'
    UNDETERMINED = 'undetermined'

    MATCH_RESULT_CHOICES = (
        (WHITE, 'White won'),
        (BLACK, 'Black won'),
        (DRAW, 'Match Drawn'),
        (UNDETERMINED, 'Undetermined')
    )

    round = models.ForeignKey('Round', related_name='matches', blank=True)
    white_player = models.ForeignKey('Player', related_name='match_as_white')
    black_player = models.ForeignKey('Player', related_name='match_as_black')
    result = models.CharField(max_length=20, choices=MATCH_RESULT_CHOICES, blank=True, default=UNDETERMINED)

    def __str__(self):
        return "{}(W) vs {}(B) - {}".format(self.white_player, self.black_player, self.result)


@receiver(post_save, sender=Match)
def update_player_opponents_and_score(sender, instance, **kwargs):
    points_map = {
        Match.WHITE: 1,
        Match.BLACK: 0,
        Match.DRAW: 0.5
    }

    white = instance.white_player
    black = instance.black_player
    white.opponents.add(black)
    black.opponents.add(white)
    if instance.result is not Match.UNDETERMINED:
        white.score += points_map[instance.result]
        black.score += abs(1-points_map[instance.result])
    white.save()
    black.save()



# class PlayerColor(models.Model):
#
#     WHITE = 'White'
#     BLACK = 'Black'
#
#     COLOR_CHOICES = (
#         (WHITE, 'White'),
#         (BLACK, 'Black')
#     )
#
#     player = models.ForeignKey('Player')
#     match = models.ForeignKey('Match')
#     color = models.CharField(max_length=10, choices=COLOR_CHOICES)
