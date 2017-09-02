from django.contrib import admin
from .models import (Player, Tournament, Round, Match, )


admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Match)

