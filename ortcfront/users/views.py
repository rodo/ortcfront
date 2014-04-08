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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ortcfront.rules.models import Domain, Rule
from ortcfront.alerts.models import Alert, Notification, Subscription

logger = logging.getLogger(__name__)


def home(request):
    """The home page
    """
    alerts = Alert.objects.filter(enable=True).order_by('-create_on')
    return render(request,
                  'home.html',
                  {'alerts': alerts})


@login_required
def profile(request):
    """The home page
    """
    domains = Domain.objects.filter(enable=True).order_by('-created')
    notification = Notification.objects.filter(user=request.user).order_by('-date')
    my_subscriptions = Subscription.objects.filter(user=request.user)
    return render(request,
                  'profile.html',
                  {'my_domains': domains,
                   'my_subscriptions': my_subscriptions})
