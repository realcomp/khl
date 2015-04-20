#coding: utf-8
from rest_framework import pagination
from rest_framework import serializers


class NextPageField(serializers.Field):
    page_field = 'page'
    def to_representation(self, value):
        if value.has_next():
            return value.next_page_number()


class PreviousPageField(serializers.Field):
    page_field = 'page'
    def to_representation(self, value):
        if value.has_previous():
            return value.previous_page_number()


# class AltPaginationSerializer(pagination.PaginationSerializer):
#     next_page = NextPageField(source='*')
#     previous_page = PreviousPageField(source='*')
