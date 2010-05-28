#!/usr/bin/python2.6
import sys, os
from os.path import expanduser


# Add a custom Python path.
sys.path.insert(0, expanduser("/home/jared/python"))
import deps

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

# Switch to the directory of your project. (Optional.)
sys.path.insert(1, expanduser('/home/jared/clone/gamecc/gameccorg'))
sys.path.insert(1, expanduser('/home/jared/clone/gamecc'))
os.chdir(expanduser('/home/jared/clone/gamecc/gameccorg'))

import settings
deps.add_all_to_path(settings, auto_update=False)
# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

