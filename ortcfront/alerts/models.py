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
from django.conf import settings
from django.db import models
from django.core.mail import mail_admins
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.geos import GEOSGeometry
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from ortcfront.rules.models import Domain, Rule


class Geozone(models.Model):
    """Geographical zone to filter alerts
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    create_by = models.ForeignKey(User)
    create_on = models.DateTimeField(auto_now_add=True)

    geom = gismodels.MultiPolygonField()

    objects = gismodels.GeoManager()

    def model(self):
        return "Geo Zone"

    def get_absolute_url(self):
        return reverse("geozone_view", kwargs={'pk': self.id})

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
    name = models.CharField(max_length=50)
    description = models.TextField()
    domain = models.ForeignKey(Domain)
    geozone = models.ForeignKey(Geozone)

    # is the alert enable or not
    enable = models.BooleanField(default=True)

    # do stats are compute on this alert
    stat = models.BooleanField(default=False)

    #
    create_by = models.ForeignKey(User)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    def get_rules(self):
        return Rule.objects.filter(domains=self.domain)

    def get_events(self):
        return Event.objects.filter(alert=self).order_by('-date_event')

    def last_events(self):
        return Event.objects.filter(alert=self).order_by('-date_event')[:20]

    def get_absolute_url(self):
        return "/alert/{}/".format(self.id)

    def get_subscribers(self):
        return Subscription.objects.filter(alert=self)

    def nb_subscribers(self):
        return Subscription.objects.filter(alert=self).count()

    def nb_notifications(self):
        return Notification.objects.filter(alert=self).count()

    def synopsis(self):
        """Main information in a little string
        """
        return render_to_string("alerts/alert_synopsis.txt",
                                {'item': self})

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
    alert = models.ForeignKey(Alert)
    rule = models.ForeignKey(Rule)

    status = models.PositiveSmallIntegerField(default=1,
                                              choices=((1, 'new'),
                                                       (2, 'info'),
                                                       (3, 'validate'),
                                                       (4, 'error'),
                                                       ))

    item = models.PositiveSmallIntegerField(choices=((1, 'node'),
                                                     (2, 'way'),
                                                     (3, 'relation')))

    action = models.PositiveSmallIntegerField(choices=((1, 'create'),
                                                       (2, 'delete'),
                                                       (3, 'tagchange'),
                                                       (4, 'tagdelete'),
                                                       (5, 'tagcreate'),
                                                       (6, 'topochange')))

    osmid = models.BigIntegerField()
    changeset = models.BigIntegerField()
    #
    change = models.TextField(blank=True, null=True)
    #
    geom = gismodels.GeometryField()
    # non mandatory fields
    date_event = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    date_processed = models.DateTimeField(auto_now_add=False,
                                          blank=True,
                                          null=True)

    class Meta:
        unique_together = ('alert', 'rule', 'osmid', 'changeset')

    def get_absolute_url(self):
        return "/event/{}/".format(self.id)

    def status_icon(self):
        statuses = {'3': 'ok',
                    '2': 'info',
                    '1': 'question',
                    '4': 'error'}
        return statuses[str(self.status)]

    def status_str(self):
        statuses = {'1': 'new',
                    '2': 'need info',
                    '3': 'validate',
                    '4': 'error'}
        return statuses[str(self.status)]

    def action_str(self):
        actions = {'1': 'create',
                   '2': 'delete',
                   '3': 'tagchange',
                   '4': 'tagdelete',
                   '5': 'tagcreate',
                   '6': 'topochange'}
        return actions[str(self.action)]

    def get_osmid_img(self):
        """Build a string represents osm img
        """
        setting = settings.OSM_ITEMS[str(self.item)]
        return "20px-Osm_element_{}.svg.png".format(setting)

    def get_osmid_url(self):
        return "{}/{}/{}".format(settings.OSM_WWW,
                                 settings.OSM_ITEMS[str(self.item)],
                                 self.osmid)

    def get_changeset_url(self):
        return "{}/changeset/{}".format(settings.OSM_WWW,
                                        self.changeset)


class Report(models.Model):
    """An report made on an event
    """
    author = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    comment = models.TextField()

    status = models.PositiveSmallIntegerField(default=3,
                                              choices=((3, 'validate'),
                                                       (2, 'info'),
                                                       (4, 'error'),
                                                       ))

    create_on = models.DateTimeField(auto_now_add=True)

    def status_str(self):
        statuses = {'1': 'new',
                    '2': 'need info',
                    '3': 'validate',
                    '4': 'error'}
        return statuses[str(self.status)]


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


def inform_admin(sender, instance, created, **kwargs):
    if created:
        mail_admins("New alert created",
                    instance.synopsis())


post_save.connect(analyze_event, sender=Event)
post_save.connect(auto_subscribe_alert, sender=Alert)
post_save.connect(inform_admin, sender=Alert)
