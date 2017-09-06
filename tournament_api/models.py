from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    # winner = models.ForeignKey('Player', null=True, blank=True, related_name='tournament_won')

    def __str__(self):
        return self.name

    def get_standings(self):
        return self.player_set.all().order_by('score')


class Round(models.Model):

    tournament = models.ForeignKey('Tournament')
    round_num = models.IntegerField()

    class Meta:
        unique_together = ("tournament", "round_num")

    def __str__(self):
        return "{} - Round {} ".format(self.tournament, self.round_num)

    def get_pairings(self):
        matched = set()
        current_standings = Tournament.objects.get(round=self).get_standings()
        pairings = []
        for i, player1 in enumerate(current_standings):
            if player1 not in matched:
                for player2 in current_standings[i+1:]:
                    if player2 not in player1.opponents.all() and player2 not in matched:
                        pairings.append((player1.id, player2.id))
                        matched.add(player1)
                        matched.add(player2)
                        break
        return pairings


class Match(models.Model):

    WHITE = 'White'
    BLACK = 'Black'
    DRAW = 'Draw'
    UNDETERMINED = 'Undetermined'

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
        'White': 1,
        'Black': 0,
        'Draw': 0.5
    }

    white = instance.white_player
    black = instance.black_player
    white.opponents.add(black)
    black.opponents.add(white)
    if instance.result is not 'Undetermined':
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
