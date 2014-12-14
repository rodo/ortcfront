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
# Settings used on jenkins server
#
import os
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ortcfront',
        'USER': 'foobar',
        'PASSWORD': 'barfoo',
        'HOST': 'localhost',
        'PORT': '5432'
}


INSTALLED_APPS += (
    'django_jenkins',
    'django_nose',
)

JENKINS_TASKS = (

    )



PROJECT_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

PYLINT_RCFILE = os.path.join(PROJECT_ROOT_PATH, '..', '..', 'pylint.rc')
#
# Minimal
#
USER_AGENT = "http://exmaple.com, contact webmaster@example.com"
