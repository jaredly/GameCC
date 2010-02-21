#!/usr/bin/env python

import os

if os.environ.get('SERVER_PROTOCOL','').lower().startswith('http'):
    import ajax
    ajax.main()
else:
    import base
    base.test()
