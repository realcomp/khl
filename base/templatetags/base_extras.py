import re

from django import template
from django.contrib.admin.util import lookup_field
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.core.urlresolvers import NoReverseMatch
from django.utils.safestring import mark_safe

from suit.templatetags.suit_tags import admin_url

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, url, language):
    request = context.get('request')
    if request:
        if request.path == '/':
            return '/%s/' % language
        return re.sub(
            r'^/%s/' % request.LANGUAGE_CODE,
            '/%s/' % language, url)


@register.filter
def fcfl(admin_field):
    """Return the .contents attribute of the admin_field, and if it
    is a foreign key, wrap it in a link to the admin page for that
    object.

    Use by replacing '{{ field.contents }}' in an admin template (e.g.
    fieldset.html) with '{{ field|field_contents_foreign_linked }}'.
    """
    fieldname = admin_field.field['field']
    displayed = admin_field.contents()
    obj = admin_field.form.instance
    cond = (hasattr(admin_field.model_admin, 'linked_readonly_fields') or
            hasattr(admin_field.model_admin, 'linked_m2m_readonly_fields') or
            fieldname in admin_field.model_admin.linked_readonly_fields or
            fieldname in admin_field.model_admin.linked_m2m_readonly_fields
    )
    if not cond:
        return displayed

    try:
        fieldtype, attr, value = lookup_field(fieldname, obj,
                                              admin_field.model_admin)
    except ObjectDoesNotExist:
        fieldtype = None
    if value:
        if isinstance(fieldtype, (ForeignKey, OneToOneField)):
            try:
                url = admin_url(value)
            except NoReverseMatch:
                url = None
            if url:
                displayed = "<a href='%s'>%s</a>" % (url, displayed)
        elif isinstance(fieldtype, ManyToManyField) and admin_field.is_readonly:
            urls = ["<a href='{}'>{}</a>".format(admin_url(v), v) for v in value.all()]
            displayed = ", ".join(urls)
    return mark_safe(displayed)
