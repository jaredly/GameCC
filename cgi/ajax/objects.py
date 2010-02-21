import base

def new():
    exit({'obj':base.objects.new()})

def clone(id):
    exit({'obj':base.objects.clone(id)})

def load(id):
    exit({'obj':base.objects.load(id)})

def rename(id,new):
    base.objects.rename(id,new)
    exit()

def delete(id):
    base.objects.delete(id)
    exit()

def save_order(order):
    base.objects.save_order(order)
    exit()

def set_attr(id, attr, value):
    base.objects.set_attr(id, attr, value)
    exit()

def save_actions(id, event, actions):
    base.objects.save_actions(id, event, actions)
    exit()

def add_event(id,event):
    base.objects.add_event(id,event)
    exit()

def remove_event(id,event):
    base.objects.remove_event(id,event)
    exit()

def duplicate_event(id,event,nevent):
    actions = base.objects.duplicate_event(id,event,nevent)
    exit({'actions':actions})

def change_event(id,event,nevent):
    actions = base.objects.change_event(id,event,nevent)
    exit({'actions':actions})



