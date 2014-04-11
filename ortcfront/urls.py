from django.conf.urls import patterns, include, url
from django.contrib import admin
from .alerts.views import EventsList, EventsAPIList
from .alerts.views import EventsFeed, EventView, EventGeoJSONView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^p/', include('django.contrib.flatpages.urls')),
                       url(r'^search/', include('haystack.urls')),
                       url(r'^rule', include('ortcfront.rules.urls')),
                       url(r'^alert', include('ortcfront.alerts.urls')),
                       url(r'^events/feed/$', EventsFeed()),
                       url(r'^api/v1/events/$', EventsAPIList.as_view(), name='event_list'),
                       url(r'^events/$', EventsList.as_view(), name='event_list'),
                       url(r'^event/(?P<pk>\d+)/$', EventView.as_view(), name='event_view'),
                       url(r'^event/(?P<pk>\d+)/data.geojson$', EventGeoJSONView.as_view(), name='event_geojson'),
                       url(r'^$', 'ortcfront.users.views.home', name='home'),
                       url(r'^accounts/profile/$', 'ortcfront.users.views.profile', name='profile'),
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^admin/', include(admin.site.urls)),

)
