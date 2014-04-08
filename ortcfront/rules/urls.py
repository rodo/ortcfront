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
from .views import DomainNewView, DomainEditView, DomainView
from .views import RuleNewView, RuleEditView, RuleView, RuleListView

urlpatterns = patterns('',

                       url(r'^s/(?P<element>node|way|relation|all)/(?P<action>create|delete|modify|all]$)/', RuleListView.as_view()),
                       url(r'^s/(?P<element>node|way|relation|all)/$', RuleListView.as_view()),
                       url(r'^s/$', RuleListView.as_view()),

                       url(r'^s/domain/new/$', login_required(DomainNewView.as_view()), name='domain_new'),
                       url(r'^s/domain/(?P<pk>\d+)/edit/$', login_required(DomainEditView.as_view())),
                       url(r'^s/domain/(?P<pk>\d+)/$', DomainView.as_view()),
                       url(r'^/new/$', login_required(RuleNewView.as_view()), name='rule_new'),
                       url(r'^/(?P<pk>\d+)/edit/$', login_required(RuleEditView.as_view())),
                       url(r'^/(?P<pk>\d+)/$', RuleView.as_view()),
                       )
