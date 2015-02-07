# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class PaginationMixin(object):
    def get_paginate_by(self):
        if 'paginate_by' in self.request.GET:
            return int(self.request.GET['paginate_by'])
        return 50
