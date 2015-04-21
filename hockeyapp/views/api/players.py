from django.core.cache import cache

from rest_framework import generics, response, viewsets

from . import NumbersList
from ...filters import PlayersSearchFilter, PlayersSearchOrderFilter
from ...models import Player
from ...serializers.players import PlayersSearchSerializer, NumbersSerializer


class PlayerNumbers(NumbersList):
    serializer_class = NumbersSerializer

    def filter_queryset(self, qs):
        qs = super(PlayerNumbers, self).filter_queryset(qs)

        _player = self.request.GET.get('player')
        if _player:
            qs = qs.filter(player=_player)

        _season = self.request.GET.get('season')
        if _season:
            qs = qs.filter(season=_season)

        clubs_by_number = {}
        for clubplayer in qs.order_by('-season__start_date'):
            club = clubplayer.club
            number = clubplayer.number
            if number not in clubs_by_number:
                clubs_by_number[number] = {
                    'clubs': [],
                    'number': int(number or 0),
                }
            if club in clubs_by_number[number]['clubs']:
                i = clubs_by_number[number]['clubs'].index(club)
                c = clubs_by_number[number]['clubs'][i]
                if clubplayer not in c.clubplayers:
                    c.clubplayers.append(clubplayer)
            else:
                club.clubplayers = []
                club.clubplayers.append(clubplayer)
                clubs_by_number[number]['clubs'].append(club)

        return sorted(clubs_by_number.values(), key=lambda x: x['number'])


class PlayersSearch(viewsets.ReadOnlyModelViewSet):
    filter_backends = PlayersSearchFilter, PlayersSearchOrderFilter
    queryset = Player.objects.all()
    paginate_by = 50
    serializer_class = PlayersSearchSerializer

    def _is_default(self, request):
        if set(zip(*request.GET.items())[0]) != {'order_by', 'is_playing'}:
            return False
        if request.GET.get('order_by', '') != '%s_lastname,%s_name':
            return False
        if request.GET.get('is_playing', '') != 'true':
            return False
        return True

    def list(self, request, *args, **kwargs):
        is_default = self._is_default(request)

        if is_default:
            cached_data = cache.get(request.path)
            if cached_data and request.META.get('HTTP_PRAGMA', '') != 'no-cache':
                return response.Response(cached_data)

        qs = self.filter_queryset(self.get_queryset())
        self.rating = self._get_rating(request, qs)

        _pk = request.GET.get('player')
        if _pk:
            _pk = int(_pk)
            # qs is turned into list
            qs = qs.ranged_filter(lambda player: player.pk == _pk, 5)

        queryset = qs

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            r = self.get_paginated_response(serializer.data)
            if is_default:
                cache.set(request.path, r.data, 60*60*24)  # 1 day
            return r

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def _get_rating(self, request, qs):
        result = {}
        rating_index = 0
        if not request.GET.get('rated_by', ''):
            for player in qs:
                rating_index += 1
                result[player.pk] = rating_index
        return result


class BestPlayer(PlayersSearch):
    def retrieve(self, request, *args, **kwargs):
        instance = self.filter_queryset(self.get_queryset()).first()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)
