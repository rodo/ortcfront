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
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (DetailView, ListView, CreateView,
                                  UpdateView, TemplateView)
from django.shortcuts import get_object_or_404
from ortcfront.rules.models import Rules
from ortcfront.rules.serializers import RulesSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class RulesListView(ListView):

    model = Rules

    def get_queryset(self):
        return Rules.objects.filter(active=True)

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        else:
            return ListView.render_to_response(self, context)


def rules_list(request):
    """List all code ruless, or create a new rules.
    """
    if request.method == 'GET' or  request.method == 'HEAD':
        ruless = Rules.objects.filter(active=True)
        serializer = RulesSerializer(ruless, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RulesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    else:
        return HttpResponse("Not Implemented", status=501)
