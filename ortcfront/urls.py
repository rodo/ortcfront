from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from .alerts.views import EventsList

urlpatterns = patterns('',
                       url(r'^rule', include('ortcfront.rules.urls')),
                       url(r'^alert', include('ortcfront.alerts.urls')),
                       url(r'^events/', EventsList.as_view()),
                       url(r'^$', 'ortcfront.users.views.home', name='home'),
                       url(r'^accounts/profile/$', 'ortcfront.users.views.profile', name='profile'),
                       url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^ortcfront/', include('ortcfront.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

)
