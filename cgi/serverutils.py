
import os,sys
import myjson as json
import glob

def _make_plugin_cache():
    cached = '../plugins/all.cache'
    plugins = list((fname.split('/')[-1][:-len('.info')], json.loads(open(fname).read())) for fname in glob.glob('../plugins/*/*.info'))
    open(cached,'w').write(json.dumps(plugins))
    #return open(cached).read()

def cache_plugins():
    print 'Content-type:text/plain'
    print 'Cache-Control: max-age=3600\n'
    print _make_plugin_cache()

def load_plugins():
    fail
    plugins = glob.glob('../plugins/*/*.info')
    exit({'plugins':list(x.split('/')[-1][:-len('.info')] for x in plugins)});

if __name__=='__main__':
    if len(sys.argv)<2:
        print 'invalid'
        sys.exit()
    if sys.argv[1] == 'plugins':
        _make_plugin_cache()
