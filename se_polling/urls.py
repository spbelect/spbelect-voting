from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'se_polling.views.home', name='home'),
    # url(r'^se_polling/', include('se_polling.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('account.views',
    (r'^account/login', 'login'),
    (r'^account/logout', 'logout'),
    (r'^change-password$', 'change_password'),
)

urlpatterns += patterns('polling.views',
    (r'^index/$|^$', 'index'),
    (r'^question-list/$', 'question_list'),
    (r'^question/(?P<id>\d+)$', 'question'),
    (r'^answer/(?P<id>\d+)$', 'answer'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
      (r'^media/(?P<path>.*)$', 'django.views.static.serve',
          {'document_root': settings.MEDIA_ROOT}),
    )
