#!/usr/bin/env python
'''Main entrance -- called to do ajax, or other work.
is essentially a switch'''

import os

if os.environ.get('SERVER_PROTOCOL','').lower().startswith('http'):
    from .ajax import main
    main()
else:
    from .base import test
    test()
