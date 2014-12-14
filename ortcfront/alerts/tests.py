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
from django.test import TestCase
from ortcfront.alerts.models import Geozone
from mock import Mock, patch

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ortcfront',
        'USER': 'foobar',
        'PASSWORD': 'barfoo',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

class fakecursor(object):

    datas = ((1, 1, "un", "one"),
             (2, "deux", "two"))

    def execute(self, qry, parm=None):
        return None

    def fetchone(self):
        return self.datas[0]

    def fetchall(self):
        return self.datas

    def close(self):
        pass


class MockPg(object):
    def __init__(self, dsn):
        pass

    def set_isolation_level(self, level):
        pass

    def cursor(self):
        return fakecursor()

    def commit(self):
        pass

@patch("django.conf.settings.DATABASES", DATABASES)
@patch('psycopg2.connect', MockPg)
class AlertTests(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
