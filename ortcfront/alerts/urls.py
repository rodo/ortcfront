# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from .views import AlertNewView, AlertEditView, AlertView, AlertListView
from .views import GeozoneNewView, GeozoneEditView, GeozoneView, GeozoneGeoJSONView
from .views import ListAlerts, LatestAlertsFeed
from .models import Geozone

urlpatterns = patterns('',
                       url(r'^s/feed/$', LatestAlertsFeed()),
                       url(r'^s/$', AlertListView.as_view(), name='alert_list'),
                       url(r'^/new/$', login_required(AlertNewView.as_view()), name='alert_new'),
                       url(r'^/(?P<pk>\d+)/edit/$', login_required(AlertEditView.as_view())),
                       url(r'^/(?P<pk>\d+)/subscribe/$', 'ortcfront.alerts.views.subscribe', name='alert_subscribe'),
                       url(r'^/(?P<pk>\d+)/$', AlertView.as_view()),
                       url(r'^/zone/new/$', login_required(GeozoneNewView.as_view()), name='geozone_new'),
                       url(r'^/zone/(?P<pk>\d+)/edit/$', login_required(GeozoneEditView.as_view()), name='geozone_edit'),
                       url(r'^/zone/(?P<pk>\d+)/$', GeozoneView.as_view(), name='geozone_view'),
                       url(r'^/zone/(?P<pk>\d+)/data.geojson$', GeozoneGeoJSONView.as_view(), name='geozone_geojson'),
                       url(r'^/$', RedirectView.as_view(url='/alerts/', permanent=True)),
)
