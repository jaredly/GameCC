'''cleans the environment'''
from ..base import drupal

import subprocess
import os

def execute(cmd):
    '''execute a shell command'''
    pipe = subprocess.Popen(cmd, shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, close_fds=True)
    return (pipe.stdout.read(), pipe.stderr.read())

DR = os.path.dirname(__file__)

def clean():
    '''run the main cleaner'''
    out, err = execute(os.path.join(DR,'clean.sh') +
                  ' "%(user_db)s" "%(pwdd_db)s"'
                  ' "%(blog_db)s" "%(data_db)s"' % drupal.alls)
    if err:
        raise Exception('clean failed: %s'%err)
    print out

if __name__ == '__main__':
    clean()


