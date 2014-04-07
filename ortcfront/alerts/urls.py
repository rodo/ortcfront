from django.conf.urls import patterns, include, url

from ortcfront.alerts.views import ListAlerts

urlpatterns = patterns('',
                       url(r'^$', ListAlerts.as_view()),
)
