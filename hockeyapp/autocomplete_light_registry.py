import autocomplete_light
from .models import Player


class PlayerAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['khl_id', 'ru_fio']
    model = Player
autocomplete_light.register(PlayerAutocomplete)