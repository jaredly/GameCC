#!/usr/bin/python2.6
import sys, os
from os.path import expanduser

#print 'Content-type:text/html\n'

# Add a custom Python path.
sys.path.insert(0, expanduser("~/python"))

# Switch to the directory of your project. (Optional.)
sys.path.insert(1, expanduser('~/clone/gamecc/gameccorg'))
os.chdir(expanduser('~/clone/gamecc/gameccorg'))

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "gameccorg.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
