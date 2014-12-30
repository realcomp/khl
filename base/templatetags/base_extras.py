import re

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, url, language):
    request = context.get('request')
    if request:
        return re.sub(
            r'^/%s/' % request.LANGUAGE_CODE,
            '/%s/' % language, url)
