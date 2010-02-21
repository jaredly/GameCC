
from base import drupal

import subprocess

def execute(cmd):
    p = subprocess.Popen(cmd, shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, close_fds=True)
    return (p.stdout.read(), p.stderr.read())

def setup():
    try:drupal.get_blogdb()
    except:pass
    else:raise Exception('Blog db still there')
    try:drupal.get_datadb()
    except:pass
    else:raise Exception('Data db still there')
    o,e = execute('./setup.sh "%(user_db)s" "%(pwdd_db)s" "%(blog_db)s" "%(data_db)s"'%drupal.alls)
    if e:
        print 'Error:',e
    print o

if __name__ == '__main__':
    setup()

