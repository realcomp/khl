#coding: utf-8
from rest_framework import compat, pagination, response


class AltPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        next_page = None
        if self.page.has_next():
            next_page = self.page.next_page_number()

        previous_page = None
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()

        return response.Response(compat.OrderedDict((
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('next_page', next_page),
            ('previous', self.get_previous_link()),
            ('previous_page', previous_page),
            ('results', data),
        )))
