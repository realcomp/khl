import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', name='sitemap_xml'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if 'rest_framework' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^api-auth/',
            include('rest_framework.urls', 
            namespace='rest_framework')
        ),
    )

if 'django_select2' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^select2/', include('django_select2.urls')),
    )

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    '',
    url(r'^$', 'base.views.index', name='index'),
    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^base/', include('base.urls', namespace='base')),
    url(r'^hockey/', include('hockeyapp.urls', namespace='hockeyapp')),
)

urlpatterns += patterns('',
    url(r'^$', 'base.views.index',),
)

#TODO: remove this later
if settings.DEBUG:
    for template in os.listdir('base/templates/markup/'):
        _template = 'markup/{0}'.format(template,)
        urlpatterns += patterns('',
            url(r'^%s' % _template,
                TemplateView.as_view(template_name=_template)
            )
        )
