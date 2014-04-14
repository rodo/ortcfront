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
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import mail_admins


def inform_admins(sender, instance, created, **kwargs):
    if created:
        mail_admins("New user on osmrtcheck", "new user : {}".format(instance.username))


post_save.connect(inform_admins, sender=User)
