# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json


class PaginationMixin(object):
    def get_paginate_by(self):
        if 'paginate_by' in self.request.GET:
            return int(self.request.GET['paginate_by'])
        return 50


class OrderMixin(object):
    def filter_queryset(self, qs):
        qs = super(OrderMixin, self).filter_queryset(qs)
        if 'order_by' in self.request.GET:
            field = self.request.GET['order_by']
            is_array = (
                field.lstrip('-').startswith('[') and
                field.endswith(']'))
            if is_array:
                fields = json.loads(field.lstrip('-'))
            else:
                fields = [field.lstrip('-')]
            fields = map(
                lambda f: ('-' if field.startswith('-') else '') + (f % self.request.LANGUAGE_CODE if '%s' in f else f),
                fields)
            qs = qs.order_by(*fields)
        return qs
