import base

def new():
    exit({'obj':base.images.new()})

def clone(id):
    exit({'obj':base.images.clone(id)})

def load(id):
    exit({'obj':base.images.load(id)})

def rename(id,new):
    base.images.rename(id,new)
    exit()

def delete(id):
    base.images.delete(id)
    exit()

def save_order(order):
    base.images.save_order(order)
    exit()

def set_attr(id, attr, value):
    base.images.set_attr(id, attr, value)
    exit()
