#coding: utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView


class IndexPage(TemplateView):
    b''' Главная страница '''
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(IndexPage, self).get_context_data(**kwargs)
        return ctx
index = IndexPage.as_view()