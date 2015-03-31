
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()


SOCIAL_AUTH_BACKENDS = {
    'facebook': 'social_auth.backends.facebook.FacebookBackend',
    'twitter': 'social_auth.backends.twitter.TwitterBackend',
    'google': 'social_auth.backends.google.GoogleBackend',
    'google-oauth': 'social_auth.backends.google.GoogleOAuthBackend',
    'google-oauth2': 'social_auth.backends.google.GoogleOAuth2Backend',
    'github': 'social_auth.backends.contrib.github.GithubBackend',
    'vk-oauth': 'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'openid': 'social_auth.backends.OpenIDBackend',
}


@register.simple_tag
def social_auth_widget():
    backend_names = dict(filter(
        lambda x: x[1] in settings.AUTHENTICATION_BACKENDS,
        SOCIAL_AUTH_BACKENDS.items()))
    return ''.join('<a href="%(url)s">%(label)s</a><br/>' % {
        'url': reverse('socialauth_begin', args=(x,)),
        'label': x,
    } for x in sorted(backend_names.keys()))
