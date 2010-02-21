import base

def new():
    exit({'obj':base.maps.new()})

def clone(id):
    exit({'obj':base.maps.clone(id)})

def load(id):
    exit({'obj':base.maps.load(id)})

def rename(id,new):
    base.maps.rename(id,new)
    exit()

def delete(id):
    base.maps.delete(id)
    exit()

def save_order(order):
    base.maps.save_order(order)
    exit()

def set_attr(id, attr, value):
    base.maps.set_attr(id, attr, value)
    exit()

def add_item(id, item):
    base.maps.add_item(id, item)
    exit()

def remove_item(id, item):
    base.objects.remove_item(id, item)
    exit()

def save_items(id,items):
    base.objects.save_items(id,items)
    exit()



