# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .admin import ArenaInstaPhotoList


class ClubInstaPhotoList(ArenaInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото клуба '''
    permission_classes = ()
    def filter_queryset(self, qs):
        processed = self.request.GET.get('processed')
        if processed:
            return super(ClubInstaPhotoList, self).filter_queryset(qs)
        else:
            return qs.none()
cip_list = ClubInstaPhotoList.as_view()


class PlayerInstaPhotoList(ClubInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото игрока '''
    def filter_queryset(self, qs):
        qs = super(PlayerInstaPhotoList, self).filter_queryset(qs)
        if self.request.GET.get('player'):
            qs = qs.player_photo(self.request.GET.get('player'))
        return qs
pip_list = PlayerInstaPhotoList.as_view()


class ProcessedArenaInstaPhotoList(ClubInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото арены '''
    def filter_queryset(self, qs):
        qs = super(ProcessedArenaInstaPhotoList, self).filter_queryset(qs)
        if self.request.GET.get('arena'):
            qs = qs.arena_photo(self.request.GET.get('arena'))
        return qs
paip_list = ProcessedArenaInstaPhotoList.as_view()