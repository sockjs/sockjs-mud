from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.DJANGO_TOP_DIR + '/contrib/admin/media'}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS[0]}),

    url(r'^', include('mud.core.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
