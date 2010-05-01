#!/usr/bin/env python

import sys
import os.path
import deps

# remove '.' from the path (you should use the project package to reference 
# anything in here)
sys.path.pop(0)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if len(sys.argv) > 1 and sys.argv[1] == 'up':
    deps.add_all_to_path(settings, auto_update=True)
else:
    deps.add_all_to_path(settings, auto_update=False)

from django.core.management import execute_manager
if __name__ == "__main__":
    execute_manager(settings)
