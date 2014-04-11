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
"""

"""
import logging
from django.conf import settings
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from djgeojson.views import GeoJSONLayerView
from .models import Alert, Subscription, Geozone, Event, Report
from .serializers import AlertSerializer, EventSerializer
from .forms import AlertNewForm, GeozoneNewForm, ReportNewForm

logger = logging.getLogger(__name__)


class EventsFeed(Feed):
    title = "OpenStreetMap realtime check - Events"
    link = "/events/"
    description = "Updates on each new events."

    def get_object(self, request, alert_id=0):
        if alert_id != 0:
            return get_object_or_404(Alert, pk=alert_id)
        else:
            return None

    def items(self, obj):
        qry = Event.objects.all()
        if obj:
            qry = qry.filter(alert=obj)
        return qry.order_by('-date_event')[:20]

    def item_title(self, item):
        content = render_to_string("alerts/event_feed_title.html", 
                                   {'event': item})
        return content

    def item_description(self, item):
        content = render_to_response("alerts/event_feed_description.html",
                                     {'event': item})
        return content.content


class LatestAlertsFeed(Feed):
    title = "OpenStreetMap realtime check - Alerts"
    link = "/alerts/"
    description = "Updates on each new alert created."

    def items(self):
        return Alert.objects.order_by('-create_on')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class EventsList(ListView):
    """View to list all events
    """
    model = Event
    paginate_by=settings.ORCT_PAGINATE_DEFAULT

    def get_queryset(self):
        """Filter

        TODO : finish this filter
        """
        qry = Event.objects.all()
        try:
            status = int(self.request.GET.get('status'))
            qry = Event.objects.filter(status=status)
        except:
            pass
        return qry

                
class EventsAPIList(APIView):
    """View to list all events
    """
    authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all events
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """An event is post
        """
        logger.debug('datas  %s' % (request.DATA))
        serializer = EventSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAlerts(APIView):
    """View to list all alerts
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, format=None):
        serializer = AlertSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AlertNewView(CreateView):
    """Create a new alert
    """
    model = Alert
    template_name = 'alerts/alert_new.html'
    form_class = AlertNewForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super(AlertNewView, self).form_valid(form)


class AlertEditView(UpdateView):
    """Edit an existing alert
    """
    model = Alert
    template_name = 'alerts/alert_edit.html'
    form_class = AlertNewForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super(AlertEditView, self).get_context_data(**kwargs)
        return context


class AlertView(DetailView):
    """The public view
    """
    model = Alert

    def get_context_data(self, **kwargs):
        context = super(AlertView, self).get_context_data(**kwargs)
        return context


class EventView(DetailView):
    """The public view
    """
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['form'] = ReportNewForm()
        context['reports'] = Report.objects.filter(event=self.object).order_by('-create_on')
        return context

    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        form = ReportNewForm(request.POST)
        if form.is_valid():
            Report.objects.create(author=request.user,
                                  event=event,
                                  comment=form.cleaned_data['comment'],
                                  status=form.cleaned_data['status'])
            event.status = form.cleaned_data['status']
            event.save()

        return HttpResponseRedirect(reverse('event_view', args=[pk]))


class ListAlerts(APIView):
    """View to list all alerts
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        alerts = Alert.objects.filter(enable=True)
        domainid = self.request.GET.get('domain')
        if domainid:
            alerts = alerts.filter(domain__id=domainid)

        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


class AlertListView(ListView, ListAlerts):
    """List all the rules
    """
    model = Alert
    paginate_by=settings.ORCT_PAGINATE_DEFAULT

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            return ListAlerts.get(self, self.request)
        else:
            # Look for a 'format=json' GET argument
            return ListView.render_to_response(self, context)


class GeozoneNewView(CreateView):
    """Create a new geozone
    """
    model = Geozone
    template_name = 'alerts/geozone_new.html'
    form_class = GeozoneNewForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super(GeozoneNewView, self).form_valid(form)


class GeozoneEditView(UpdateView):
    """Edit an existing geozone
    """
    model = Geozone
    template_name = 'alerts/geozone_edit.html'
    form_class = GeozoneNewForm
    success_url = reverse_lazy('profile')


class GeozoneView(DetailView):
    """The public view
    """
    model = Geozone

    def get_context_data(self, **kwargs):
        context = super(GeozoneView, self).get_context_data(**kwargs)
        return context


class GeozoneGeoJSONView(GeoJSONLayerView):
    model = Geozone

    def get_queryset(self):
        return Geozone.objects.filter(pk=self.kwargs['pk'])


class EventGeoJSONView(GeoJSONLayerView):
    model = Event

    def get_queryset(self):
        return Event.objects.filter(pk=self.kwargs['pk'])



@login_required
def subscribe(request, pk):
    """The home page
    """
    alert = Alert.objects.get(pk=pk)
    Subscription.objects.create(user=request.user,
                                alert=alert)

    return redirect(alert.get_absolute_url())
