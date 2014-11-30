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
from time import mktime, strptime
from datetime import datetime
from ortcfront.alerts.models import Alert


class AlertUserStats(models.Model):
    """
    element : node / way / relation
    action : create / delete / modify    
    """
    alert = models.ForeignKey(Alert)
    date_stat = models.DateField()

    item = models.PositiveSmallIntegerField(choices=((1, 'node'),
                                                     (2, 'way'),
                                                     (3, 'relation')))

    created = models.IntegerField(default=0)
    modified = models.PositiveIntegerField(default=0)
    deleted = models.PositiveIntegerField(default=0)
    userid = models.BigIntegerField(default=0)
    # update by trigger
    month = models.PositiveSmallIntegerField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        dt_object = datetime.fromtimestamp(mktime(strptime(self.date_stat,'%Y-%m-%d'))) 
        
        self.month = dt_object.month
        self.year = dt_object.year
        super(AlertUserStats, self).save(*args, **kwargs)


class AlertStats(models.Model):
    """
    Filled by Trigger    
    """
    alert = models.ForeignKey(Alert)
    date_stat = models.DateField()
    item = models.PositiveSmallIntegerField(choices=((1, 'node'),
                                                     (2, 'way'),
                                                     (3, 'relation')))
    created = models.IntegerField(default=0)
    modified = models.PositiveIntegerField(default=0)
    deleted = models.PositiveIntegerField(default=0)
    # update by trigger
    month = models.PositiveSmallIntegerField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)


class ViewAlertYear(models.Model):
    """This is a SQL VIEW

    """
    alert_id = models.IntegerField()
    year = models.IntegerField()
    created = models.IntegerField(default=0)
    modified = models.PositiveIntegerField(default=0)
    deleted = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'stats_view_alert_year'
        managed = False


    def __unicode__(self):
        return u"alert %s, year %s" % (self.alert_id, self.year)

class ViewAlertUser(models.Model):
    """Stats by users

    """
    alert_id = models.IntegerField()
    date_stat = models.DateField()
    created = models.IntegerField(default=0)
    modified = models.PositiveIntegerField(default=0)
    deleted = models.PositiveIntegerField(default=0)
    userid = models.BigIntegerField(default=0)
    item = models.CharField(max_length=10)
    item_id = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=0)
    month = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'stats_view_users'
        managed = False


    def __unicode__(self):
        return u"alert %s, year %s" % (self.alert_id, self.year)


class OsmUser(models.Model):
    """Stats by users

    """
    osm_uid = models.BigIntegerField()
    username = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % (self.username)
