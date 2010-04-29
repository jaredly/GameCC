'''setup the environment -- mostly SQL stuff'''
from base import drupal

import subprocess

def execute(cmd):
        '''execute a shell command'''
            pipe = subprocess.Popen(cmd, shell=True,
                                        stdin=subprocess.PIPE,
                                                            stdout=subprocess.PIPE,
                                                                                stderr=subprocess.PIPE, close_fds=True)
                return (pipe.stdout.read(), pipe.stderr.read())


def setup():
    '''run the setup'''
    try:drupal.get_blogdb()
    except:pass
    else:raise Exception('Blog db still there')
    try:drupal.get_datadb()
    except:pass
    else:raise Exception('Data db still there')
    out, err = execute('./setup.sh "%(user_db)s" "%(pwdd_db)s" '
                  '"%(blog_db)s" "%(data_db)s"'%drupal.alls)
    if err:
        print 'Error:', err
    print out

if __name__ == '__main__':
    setup()

