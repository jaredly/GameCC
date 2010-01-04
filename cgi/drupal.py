#!/usr/bin/env python

import os,sys

import myjson as json

sys.path.append('/home1/marketr5/lib64/python2.4/site-packages')

import MySQLdb

pwdfile = '/home/jared/clone/.liveframe'
#print 'Content-type:text/html\n'

if not os.path.isfile(pwdfile):
    print 'Content-type:text/html\n'
    raise Exception,'Server configuration exception: pwd file not found'

from ConfigParser import ConfigParser as CP

parser = CP()
parser.read(pwdfile)
alls = dict(parser.items('gamecc'))

## globals

loggedin = False
username = ''
uid      = 0
db       = None
pid      = None

schemas = {
    'projects':(
        ('pid','serial'),
        ('uid','int'),
        ('name','text'),
        ('images','text'),
        ('config','text'),
    ),
    'images':(
        ('pid','int'),
        ('name','text'),
        ('subimages','text'),
        ('speed','int'),
    ),
    'objects':(
        ('pid','int'),
        ('name','text'),
        ('visible','text'),
        ('image','text'),
        ('events','text'),
        ('attributes','text'),
        ('parent','text'),
    ),
    'maps':(
        ('pid','int'),
        ('name','text'),
        ('objects','text'),
        ('width','int'),
        ('height','int'),
        ## ('fps','int'),
        ('events','text'),
        ('tiles','text'),
        ('views','text'),
        ('_index','int'),
        ('background','int'),
    ),
    'ratings':(
        ('pid','int'),
        ('type','text'),
        ('uid','int'),
        ('name','text'),
        ('rating','int')
    )
}

def check_tables():
    good = {}
## ^ for later schema checking
    for name,schema in schemas.items():
        try:
            #db.execute('drop table %s'%name)
            db.execute_dict('select * from %s limit 1'%name)
            good[name] = True
        except:
            db.execute('create table %s ( %s )'%(name,', '.join(' '.join(a) for a in schema)))

class MySQL:
    def __init__(self, db):
        self.db = MySQLdb.connect("localhost", alls['user_db'], alls['pwdd_db'], db)
        self.cursor = self.db.cursor()
        self.dcursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        self.db.quit()

    def _fill(self, dct):
        if not dct.has_key('pid') and pid:
            dct['pid'] = pid

    def serialize(self, x):
        if type(x) in (int,float,long):
            return str(x)
        if x is None:return 'NULL'
        return "'%s'" % json.dumps(x).replace('\\','\\\\').replace("'","\\'")

    def insert_dict(self, table, dct):
        self.cursor.execute('insert into %s set '%table+', '.join('%s=%s'%(k, self.serialize(v)) for k,v in dct.items()))
        self.db.commit()

    def insert(self, table, lst):
        self.cursor.execute('insert into %s values ('%table+', '.join(self.serialize(v) for v in lst) + ')')
        self.db.commit()

    def update(self, table, dct, cond = {1:1}):
        self._fill(cond)
        vbls = ', '.join('%s=%s'%(k, self.serialize(v)) for k,v in dct.items())
        conds = ' and '.join('%s=%s'%(k, self.serialize(v)) for k,v in cond.items())
        #print 'update %s set '%table + vbls + ' where %s'%conds
        self.cursor.execute('update %s set '%table + vbls + ' where %s'%conds)
        self.db.commit()

    def delete(self, table, dct):
        self._fill(dct)
        self.cursor.execute('delete from %s where %s'%(table, ' and '.join('%s=%s'%(k, self.serialize(v)) for k,v in dct.items())))
        self.db.commit()

    def unserialize(self, x):
        if type(x) in (int,float):
            return x
        if type(x) == long:
            return int(x)
        return json.loads(x)

    def find(self, table, dct={1:1}, names = ['*'], order=''):
        if order:order=' order by '+order
        self._fill(dct)
        return self.execute('select %s from %s where %s%s'%(','.join(names), table, ' and '.join('%s=%s'%(k, self.serialize(v)) for k,v in dct.items()), order))

    def find_dict(self, table, dct={1:1}, names = ['*'], order=''):
        if order:order=' order by '+order
        self._fill(dct)
        return self.execute_dict('select %s from %s where %s%s'%(','.join(names), table, ' and '.join('%s=%s'%(k, self.serialize(v)) for k,v in dct.items()), order))

    def execute(self, cmd):
        self.cursor.execute(cmd)
        return list(list(self.unserialize(x) for x in row) for row in self.cursor.fetchall())

    def execute_dict(self, cmd):
        self.dcursor.execute(cmd)
        return list(dict((k, self.unserialize(v)) for k,v in row.items()) for row in self.dcursor.fetchall())

    def commit(self):
        self.db.commit()

def getcookies():
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE']
        cookies = cookies.split('; ')
        handler = {}
        for cookie in cookies:
            cookie = cookie.split('=')
            handler[cookie[0]] = cookie[1]
        return handler
    return {}

def getpid(name):
    global pid
    res = db.find('projects',{'uid':uid,'name':name},['pid'])
    #res = db.execute("select pid from projects where uid=%d and name='%s'"%(uid, name))
    if not res:
        pid = None
    else:
        pid = res[0][0]

def altlogin(form):
    global loggedin, username, uid, db, pid
    cookies = getcookies()
    db = MySQLdb.connect("localhost", alls['user_db'], pwd, alls['blog_db'])
    cursor = db.cursor()
    u = form['username'].value
    p = form['password'].value
    cursor.execute("select uid from users where name='%s' and pass='%s'"%(u,p))
    res = cursor.fetchall()
    if not res:
        return False
    loggedin = True
    username = u
    uid = res[0][0]
    db = MySQL(alls['data_db'])
    return True

def login():
    global loggedin, username, uid, db, pid
    cookies = getcookies()
    db = MySQLdb.connect("localhost", alls['user_db'], alls['pwdd_db'], alls['blog_db'])
    cursor = db.cursor()
    for cookie in cookies:
        if cookie.startswith('SESS'):
            cursor.execute('select * from sessions where sid="'+cookies[cookie]+'"')
            sess = cursor.fetchone()
            if sess:
                cursor.execute('select name from users where uid=%d'%sess[0])
                name = cursor.fetchone()[0]
                if not name:continue
                loggedin = True
                uid = sess[0]
                username = name
                db = MySQL(alls['data_db'])
                check_tables()
                return True
    loggedin = False
    username = ''
    uid      = 0
    db       = None
    return False

