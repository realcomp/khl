#coding: utf-8
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib import admin
#from django.contrib.admin.utils import reverse_field_path
from django.db import models
from django.utils.translation import ugettext_lazy as _

#import autocomplete_light
#from django_select2.fields import Select2ChoiceField
from django_select2.widgets import Select2MultipleWidget, Select2Widget
from suit.admin import SortableModelAdmin
from suit.widgets import LinkedSelect, SuitDateWidget, SuitSplitDateTimeWidget

from .models import Season, TitleAlias, SocialNetValue, InstagramImageFile


DEFAULT_FORMTABS = (('general', 'General'),)+settings.LANGUAGES
select2_options = {'width': 'resolve', 'dropdownAutoWidth': True,}

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
            'widget': LinkedSelect2(select2_options=select2_options)
        },
        models.OneToOneField: {
            'widget': LinkedSelect2(select2_options=select2_options)
        },
        models.ManyToManyField: {
            'widget': Select2MultipleWidget(select2_options=select2_options)
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
    
class BaseListAdmin(BaseAdmin):
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


class TabularInlineReadOnly(NoActionMixin, BaseMixin, admin.TabularInline):
    extra=0
    max_num=0
    can_delete=False


class AutocompleteFieldFilter(admin.filters.AllValuesFieldListFilter):
    template = 'admin/autocomplete_filter.html'


class FromToForm(forms.Form):
    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        placeholder = kwargs.pop('placeholder', field_name)
        super(FromToForm, self).__init__(*args, **kwargs)
        widget = forms.widgets.TextInput
        placeholder_from = '{} {}'.format(placeholder, _('From'))
        self.fields['%s__gte' % field_name] = forms.CharField(
                label='',
                widget = widget(attrs={'placeholder': placeholder_from}),
                required=False)
        placeholder_to = '{} {}'.format(placeholder, _('To'))
        self.fields['%s__lte' % field_name] = forms.CharField(
                label='',
                widget = widget(attrs={'placeholder': placeholder_to}),
                required=False)


class SimpleRangeFilter(admin.filters.FieldListFilter):
    template = 'admin/simplerange_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super(SimpleRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.placeholder = self.title
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        return FromToForm(  data=self.used_parameters,
                            field_name=self.field_path,
                            placeholder=self.placeholder
        )

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: bool(x[1]),
                                        self.form.cleaned_data.items()))
            return queryset.filter(**filter_params)
        else:
            return queryset
#admin.filters.FieldListFilter.register( lambda f: True, SimpleRangeFilter)


for m in (TitleAlias, Season, SocialNetValue, InstagramImageFile):
    admin.site.register(m, BaseAdmin)