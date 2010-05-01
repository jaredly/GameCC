#!/usr/bin/env python
import os
import deps

PROJECT_PATH = os.path.abspath('%s/..' % os.path.dirname(__file__))

DEPENDENCY_ROOT = os.path.join(PROJECT_PATH, 'external')
DEPENDENCIES = (
    # subversion
    deps.SVN(
        'http://django-rabid-ratings.googlecode.com/svn/trunk/rabidratings',
        app_name='rabidratings',
        root=DEPENDENCY_ROOT,
    ),
    deps.SVN(
        'http://django-navbar.googlecode.com/svn/trunk/',
        app_name='navbar',
        root=DEPENDENCY_ROOT,
    ),
    # mercurial
    # deps.HG(),
    # git pinned to a SHA1 id with rev can use HEAD or other tags
    # deps.GIT(),
)

# vim: et sw=4 sts=4
