# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os, time
import subprocess
from django.apps import apps
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = "Build the front with bower and gulp"

    def add_arguments(self, parser):

        parser.add_argument(
            '--force-npm',
            action='store_true',
            dest='force_npm',
            default=False,
            help='force npm install',
        )

        parser.add_argument(
            '--force-bower',
            action='store_true',
            dest='force_bower',
            default=False,
            help='force bower install',
        )

    def handle(self, *args, **options):
        self.force_npm = options['force_npm']
        self.force_bower = options['force_bower']
        app_path = os.sep.join([apps.get_app_config('timeside_player').path, 'static', 'timeside2'])
        os.chdir(app_path)
        print('Building front...')
        os.system('npm install -g grunt')
        os.system('npm cache clean -f; npm install -g n; n stable')
        if not os.path.exists('node_modules') or self.force_npm:
            os.system('npm install')
        os.system('grunt build --force')