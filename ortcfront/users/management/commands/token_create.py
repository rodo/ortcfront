#!/usr/bin/python
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
User management
"""
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Print tools on stdout'

    def handle(self, *args, **options):
        """
        Update the number of points of all users
        """
        user = None
        username = sys.argv[2]
        try:
            user = User.objects.get(username=username)
        except:
            self.stdout.write('No user with username : {}\n'.format(username))

        if user:
            try:
                token = Token.objects.create(user=user)
                print token.key
            except:
                pass

