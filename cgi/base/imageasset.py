'''image asset. used to test general asset stuff

>>> img = new()
>>> id = img['id']
>>> id
1
>>> img['name']
u'Image'
>>> img2 = clone(id)
>>> img2['name']
u'Image_Copy'
>>> id2 = img2['id']
>>> id2
2
>>> load(id)['id'] == id
True
>>> rename(id, 'Gonzalez')
>>> load(id)['name']
u'Gonzalez'
>>> delete(id)
>>> load(id)
Traceback (most recent call last):
...
AssetException: Asset 1 of type "images" not found

'''
import asset

#good: Jan 4

class ImageManager(asset.AssetManager):
    atype = 'images'
    defaults = {'speed':1,'subimages':[]}

'''
def fromurl(project,url):
  id = url.split('/')[-1]
  saveraw(project, id, upen(url).read())
  exit({'id':id})

def saveraw(project,id,data):
  if os.path.isfile(os.path.join('../projects',project,'images',id)):
    parts = id.split('.')
    id = '.'.join(parts[:-1])
    ext = parts[-1]
    i=1
    while os.path.isfile(os.path.join('../projects',project,'images',id+'-'+str(i)+'.'+ext)):
      i+=1
    id += '-'+str(i)+'.'+ext
  open(os.path.join('../projects',project,'images',id),'w').write(data)

def importimages(project,urls):
  urls = json.loads(urls)
  for src in urls:
    src = os.path.join('..',src)
    saveraw(project, src.split('/')[-1], open(src).read())
  exit()

def loadraw(project):
  exit({'images':list(x.split('/')[-1] for x in glob.glob('../projects/'+project+'/images/*.*') if x.split('.')[-1] in ('png','gif','jpg'))})
'''
