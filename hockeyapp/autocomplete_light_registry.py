import autocomplete_light
from .models import Player, Club


class PlayerAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['khl_id', 'ru_fio']
    model = Player
autocomplete_light.register(PlayerAutocomplete)


class ClubAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = Club
    search_fields = ['ru_title',]
autocomplete_light.register(ClubAutocomplete)