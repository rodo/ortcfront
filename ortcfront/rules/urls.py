from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'ortcfront.rules.views.rules_list'),
)
