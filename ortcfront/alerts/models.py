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
Models definition
"""
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.geos import GEOSGeometry
from ortcfront.rules.models import Domain, Rule


class Geozone(models.Model):
    """Geographical zone to filter alerts
    """

    name = models.CharField(max_length=30)
    description = models.TextField()

    create_by = models.ForeignKey(User)
    create_on = models.DateTimeField(auto_now_add=True)

    geom = gismodels.MultiPolygonField()

    objects = gismodels.GeoManager()

    def __unicode__(self):
        """The unicode method
        """
        return self.name

    def __str__(self):
        """The string method
        """
        return self.name


class Alert(models.Model):
    """
    """
    name = models.CharField(max_length=30)
    description = models.TextField()
    domain = models.ForeignKey(Domain)
    geozone = models.ForeignKey(Geozone)

    # is the alert enable or not
    enable = models.BooleanField(default=True)

    #
    create_by = models.ForeignKey(User)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    def get_rules(self):
        return Rule.objects.filter(domains=self.domain)

    def get_absolute_url(self):
        return "/alert/{}/".format(self.id)

    def get_subscribers(self):
        return Subscription.objects.filter(alert=self)

    def nb_subscribers(self):
        return Subscription.objects.filter(alert=self).count()

    def nb_notifications(self):
        return Notification.objects.filter(alert=self).count()

    def __unicode__(self):
        """The unicode method
        """
        return self.name

    def __str__(self):
        """The string method
        """
        return self.name


class Event(models.Model):
    """An event pushed on the platform by osmrtcheck
    """
    rule = models.ForeignKey(Rule)
    item = models.PositiveSmallIntegerField(choices=((1, 'node'),
                                                     (2, 'way'),
                                                     (3, 'relation')))
    osmid = models.BigIntegerField()
    changeset = models.BigIntegerField()
    #
    geom = models.TextField(blank=True, null=True)
    # non mandatory fields
    date_event = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    date_processed = models.DateTimeField(auto_now_add=False,
                                          blank=True,
                                          null=True)

    class Meta:
        unique_together = ('rule', 'osmid', 'changeset')


class Subscription(models.Model):
    """
    """
    user = models.ForeignKey(User)
    alert = models.ForeignKey(Alert)
    create_on = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    """
    """
    user = models.ForeignKey(User)
    alert = models.ForeignKey(Alert)
    create_on = models.DateTimeField(auto_now_add=True)


def analyze_event(sender, instance, created, **kwargs):
    # instance (models.Event)
    if created:
        domains = instance.rule.domains.all()
        alerts = Alert.objects.filter(domain__in=domains)
        # instance['geom'] is a string here
        geom = GEOSGeometry(instance.geom)
        alerts = alerts.filter(geozone__geom__contains=geom)
        for alert in alerts:
            for sub in Subscription.objects.filter(alert=alert):
                Notification.objects.create(user=sub.user,
                                            alert=alert)

def auto_subscribe_alert(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(user=instance.create_by,
                                    alert=instance)

post_save.connect(analyze_event, sender=Event)
post_save.connect(auto_subscribe_alert, sender=Alert)
