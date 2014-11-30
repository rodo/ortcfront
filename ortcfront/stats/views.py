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
import json
from django.conf import settings
from django.views.generic import DetailView
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
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r

from ortcfront.utils.view import CSVResponseMixin
from ortcfront.stats.models import ViewAlertYear


logger = logging.getLogger(__name__)


class AlertYearCsv(CSVResponseMixin):
    """View to list all events
    """
    renderer_classes = (r.CSVRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)


class DataView(CSVResponseMixin, DetailView):

    def get(self, request, *args, **kwargs):
        data = (('hello', 'world'), ('foo', 'bar'))
        return self.render_to_csv(data)

