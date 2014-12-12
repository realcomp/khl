from django.contrib import admin

from base.admin import BaseAdmin, BaseMixin

from .models import Player, Coach, Judge, Club, Match
from .models import MatchGoalHistory, MatchPenaltyHistory, ClubPlayer


class GoalEntryInline(BaseMixin, admin.StackedInline):
    model = MatchGoalHistory
    extra=0

class PenaltyEntryInline(BaseMixin, admin.TabularInline):
    model = MatchPenaltyHistory
    extra=0

class MatchAdmin(BaseAdmin):
    inlines = (GoalEntryInline, PenaltyEntryInline)
    list_display = 'khl_id', 'ru_title', 'url', 'spectators', 'date', 'count'

    def get_list_filter(self, request):
        if self.list_filter:
            return self.list_filter
        if self.list_display:
            return self.list_display   
        return self.get_fields(request)
        
    def get_list_display(self, request):
        if self.list_display:
            return self.list_display
        return ('id',)+self.get_fields(request)
admin.site.register(Match, MatchAdmin)

for model in (Player, Coach, Judge, MatchGoalHistory, MatchPenaltyHistory,
Club, ClubPlayer):
    admin.site.register(model, BaseAdmin)