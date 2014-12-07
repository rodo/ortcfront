#!/usr/bin/env python
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
import sys
import csv
from django.core.management.base import BaseCommand
from optparse import make_option
from django.conf import settings
from ortcfront.stats.models import OsmUser
from ortcfront.alerts.models import Alert, Domain, Geozone
import requests
import json
from shapely.geometry import mapping, shape
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import MultiPolygon, Polygon


class Command(BaseCommand):
    help = 'Import datas'
    option_list = BaseCommand.option_list + (
        make_option("-p",
                    "--project",
                    dest="project_id",
                    type="int",
                    help="project id to import",
                    default=None),
        )

    def parsejson(self):
        """Parse geojson
        """
        d = json.loads(self.content)

        area = None

        for geom in d['features']:
            s = shape(geom['geometry'])
            if area:
                area = area.union(s)
            else:
                area = s
        return area

    def handle(self, *args, **options):
        """
        Read the table with a TextField but not using it

        http://tasks.hotosm.org/project/767/tasks.json
        """
        self.project_id = options['project_id']
        if not options['project_id']:
            sys.stdout.write("exit")
            sys.exit(0)

        self.content = self.dljson()
        if self.content:
            self.shape = self.parsejson()
            self.create_alert()

    def create_alert(self):
        """Create the Alert in database
        """
        nb = Alert.objects.all().count()
        gzon = self.create_geozone()
        alert = Alert.objects.create(name="Hot project nb %s" % (self.project_id),
                                     domain_id=settings.IMPORT_DOMAIN_ID,
                                     geozone=gzon,
                                     dyn_attr={'hot_project': self.project_id},
                                     create_by_id=settings.IMPORT_USER_ID)
        sys.stdout.write("alert %s created\n" % (alert.id))

    def create_geozone(self):
        bounds = self.shape.bounds

        p2 = Polygon( ((bounds[0], bounds[1]),
                       (bounds[0], bounds[3]),
                       (bounds[2], bounds[3]),
                       (bounds[2], bounds[1]),
                       (bounds[0], bounds[1])))
        
        mp = MultiPolygon([p2])
        gzon = Geozone.objects.create(name="Hot Project {}".format(self.project_id),
                                      create_by_id=settings.IMPORT_USER_ID,
                                      geom=mp)
        return gzon

    def dljson(self):
        """Download project defintion from Hot Task Manager
        """
        content = None
        url = "http://tasks.hotosm.org/project/{}/tasks.json"
        headers = {'User-Agent': 'osmrtcheck'}
        req = requests.get(url.format(self.project_id,
                                      headers=headers))

        if req.status_code == 200:
            content = req.content

        return content
