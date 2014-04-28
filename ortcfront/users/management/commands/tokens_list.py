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
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Print all tokens stdout'

    def handle(self, *args, **options):
        """List tokens
        """
        logger = logging.getLogger(settings.SYSLOG_NAME)
        logger.info('list tokens')

        for token in Token.objects.all():
            self.stdout.write('{} {} \n'.format(token.user.username,
                                                token.key
                                                ))
