from rest_framework import generics


from addresses.models import Country

from ...models import League
from ...serializers import (
    CountrySerializer, CountryLeaguesSerializer, LeagueSerializer)


class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def filter_queryset(self, qs):
        qs = super(CountryList, self).filter_queryset(qs)
        s = self.request.GET.get('s')
        if s:
            qs = qs.filter(**{
                '%s_title__istartswith' % self.request.LANGUAGE_CODE: s,
            })
        return qs.order_by('%s_title' % self.request.LANGUAGE_CODE)


class CountryLeagueList(generics.ListAPIView):
    queryset = Country.objects.exclude(league__isnull=True)
    serializer_class = CountryLeaguesSerializer


class LeagueList(generics.ListAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
