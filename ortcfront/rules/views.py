# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
#
# Copyright (c) 2013,2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
import json
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.http import HttpResponse
from django.contrib.syndication.views import Feed
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import (DetailView, ListView, CreateView,
                                  UpdateView, TemplateView)
from django.shortcuts import get_object_or_404
from ortcfront.rules.models import Rule, Domain
from ortcfront.rules.forms import DomainNewForm, RuleNewForm
from ortcfront.rules.serializers import RuleSerializer
from django.core.urlresolvers import reverse, reverse_lazy
from ortcfront.alerts.models import Event


class RuleFeed(Feed):
    title = "Rules"
    link = "/rules/"
    description = "Update occurs on each new created rule."

    def items(self):
        return Rule.objects.order_by('-create_on')[:15]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        content = render_to_response("rules/rule_feed_description.html",
                                     {'item': item})
        return content.content


class JSONResponse(HttpResponse):
    """An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class RuleListView(ListView):
    """List all the rules
    """
    model = Rule

    def get_queryset(self):
        query = Rule.objects.filter(active=True).order_by('-create_on')
        if 'element' in self.kwargs.keys():
            if self.kwargs['element'] == u'node':
                query = query.filter(node_applied=True)
            if self.kwargs['element'] == u'way':
                query = query.filter(way_applied=True)
            if self.kwargs['element'] == u'relation':
                query = query.filter(relation_applied=True)
        if 'action' in self.kwargs.keys():
            if self.kwargs['action'] == u'create':
                query = query.filter(create_applied=True)
            if self.kwargs['action'] == u'delete':
                query = query.filter(delete_applied=True)
            if self.kwargs['action'] == u'modify':
                query = query.filter(modify_applied=True)
        return query

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            rules = Rule.objects.filter(active=True)
            serializer = RuleSerializer(rules, many=True)
            #return JSONResponseMixin.render_to_response(self, context)
            return JSONResponse(serializer.data)
        else:
            return ListView.render_to_response(self, context)


def rule_list(request):
    """List all rules, or create a new rules.
    """
    if request.method == 'GET' or  request.method == 'HEAD':
        rules = Rule.objects.filter(active=True)
        serializer = RuleSerializer(rules, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RuleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    else:
        return HttpResponse("Not Implemented", status=501)


class DomainNewView(CreateView):
    """Create a new domain
    """
    model = Domain
    template_name = 'rules/domain_new.html'
    form_class = DomainNewForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super(DomainNewView, self).form_valid(form)


class DomainEditView(UpdateView):
    """Edit an existing domain
    """
    model = Domain
    template_name = 'rules/domain_edit.html'
    form_class = DomainNewForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super(DomainEditView, self).get_context_data(**kwargs)
        return context


class DomainView(DetailView):
    """The public view
    Anonymous mode
    """
    model = Domain

    def get_context_data(self, **kwargs):
        context = super(DomainView, self).get_context_data(**kwargs)
        return context


class RuleNewView(CreateView):
    """Create a new rule
    """
    model = Rule
    template_name = 'rules/rule_new.html'
    form_class = RuleNewForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        logger = logging.getLogger(settings.SYSLOG_NAME)
        logger.info('{} create a new rule {}'.format(self.request.user.username,
                                                     form.cleaned_data['name']))
        form.instance.create_by = self.request.user
        return super(RuleNewView, self).form_valid(form)


class RuleEditView(UpdateView):
    """Edit an existing rule
    """
    model = Rule
    template_name = 'rules/rule_edit.html'
    form_class = RuleNewForm
    success_url = reverse_lazy('profile')


class RuleView(DetailView):
    """The public view
    """
    model = Rule

    def get_context_data(self, **kwargs):
        context = super(RuleView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.filter(rule=self.object).order_by('-date_event')[0:10]
        return context

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            domains = []
            for domain in self.object.domains.all():
                domains.append(domain.id)
            data = {'domains': domains}
            #return JSONResponseMixin.render_to_response(self, context)
            return JSONResponse(data)
        else:
            return DetailView.render_to_response(self, context)



