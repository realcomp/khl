#coding: utf-8
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models

from django_select2.widgets import Select2MultipleWidget, Select2Widget
from suit.admin import SortableModelAdmin
from suit.widgets import LinkedSelect, SuitDateWidget, SuitSplitDateTimeWidget


DEFAULT_FORMTABS = (('general', 'General'),)+settings.LANGUAGES


class LinkedSelect2(Select2Widget, LinkedSelect):
    minimumResultsForSearch = 10
    closeOnSelect = True


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        #for k,v in self.fields.items():
            #if self.fields[k].required:
                #v.widget.attrs['required']='required'
            #if k in ('title', 'desc'):
                #v.widget.attrs['style']='width: 100%;'


class BaseMixin(object):
    form = BaseForm
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.ForeignKey: {
            'widget': LinkedSelect2
        },
        models.OneToOneField: {
            'widget': LinkedSelect2
        },
        models.ManyToManyField: {
            'widget': Select2MultipleWidget(select2_options={'width': 'resolve'})
        },
    }


class NoActionMixin(object):
    def has_add_permission(self, request):
        return False

    #def has_change_permission(self, request, obj=None):
        #return False
    
    #def has_delete_permission(self, request, obj=None):
        #return False


class BaseAdmin(BaseMixin, admin.ModelAdmin):
    formtabs = DEFAULT_FORMTABS
    
    def get_list_filter(self, request, obj=None):  
        return self.get_fields(request, obj)
        
    def get_list_display(self, request, obj=None):
        return ['id',]+self.get_fields(request, obj)

    #class Media:
        #js = (
                #'js/admin.js',
        #)


class BaseAdminwithOrder(SortableModelAdmin, BaseAdmin):
    sortable='order'


class DynamicDisplayFilterMixin(object):
    def get_list_filter(self, request):
        if self.list_filter:
            return self.list_filter
        if self.list_display:
            return self.list_display   
        return self.get_fields(request)
        
    def get_list_display(self, request):
        if self.list_display:
            return self.list_display
        return ('id',)+self.get_fields(request)
        

class NoFilterAdmin(BaseAdmin):
    def get_list_filter(self, request, obj=None):  
        return