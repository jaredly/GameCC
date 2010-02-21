import base
import glob

def execute(cmd):
    p = subprocess.Popen(cmd, shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, close_fds=True)
    stdout, stderr = (p.stdout.read(), p.stderr.read())
    if stderr or stdout:
        die(stdout + stderr)

def list_projects():
    projects = base.project.list_projects()
    exit({'projects':projects});


def list_images():
    images = base.project.list_images()
    exit({'images':images})

def add_images(images):
    base.project.add_images(images)
    exit()

def list_all_images():
    images = base.project.list_all_images()
    exit({'images':images})

noproject = ['project/new','project/list_projects','project/load_plugins']

def new(name):
    if not base.project.new(name):
        die('Duplicate name')
    else:
        load(name)

def remove():
    base.project.remove()
    exit()

def load(name):
    drupal.pid = drupal.db.find('projects',{'name':name,'uid':drupal.uid},['pid'])[0][0]
    exit(base.project.load())

def uploadimage(file):
    filename = base.project.uploadimage(file)
    if filename is None:
        die('Invalid image file')
    sys.stdout.write(filename)

def preview():
    base.project.preview()

'''
    compiler = compile.Compiler(pid)


    die('notimplemented')
    #compiler = compile.Compiler(pid)
    #name = compiler.compile('haxe')
    data = {'name':name,'width':compiler.width,'height':compiler.height,'fps':40,'color':'ffffff'}
    cmd = '~/haxe -swf ../preview/%(name)s.swf -main %(name)s -swf-version 9 -swf-header %(width)s:%(height)s:%(fps)s:%(color)s'%data
    execute(cmd)
    execute('cat ../data/default.html | sed -e "s/<<NAME>>/%(name)s/g" -e "s/<<TITLE>>/%(name)s/g" -e "s/<<WIDTH>>/%(width)s/g" -e "s/<<HEIGHT>>/%(height)s/g" -e "s/<<COLOR>>/%(color)s/g" > ../preview/%(name)s.html'%data)
    exit({'name':name,'width':compiler.width,'height':compiler.height})
'''
