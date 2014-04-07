# -*- coding: utf-8 -*-
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
Models definition for llx app
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Domains(models.Model):
    """Domaines
    """
    name = models.CharField(max_length=30)


class Rules(models.Model):
    """
    """
    name = models.CharField(max_length=30)
    tag_regex = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    node_applied = models.BooleanField(default=False)
    way_applied = models.BooleanField(default=False)
    relation_applied = models.BooleanField(default=False)

    # Applys on actions, default all
    create_applied = models.BooleanField(default=True)
    delete_applied = models.BooleanField(default=True)
    modify_applied = models.BooleanField(default=True)

    def __unicode__(self):
        """The unicode method
        """
        return self.name

    def __str__(self):
        """The string method
        """
        return self.name

