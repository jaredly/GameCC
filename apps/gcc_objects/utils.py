#!/usr/bin/env python

from django.utils import simplejson as json
from gcc_objects.models import Object, event_vbls

## TODO: fill this in
methods = {
    'game':{}
    'object':{'angle_to':'float'}
    'globals':{'random':'function'}
}

base_types = 'int','float','str','bool','object'

def get_type(obj, attr, event, event_sub):
    parts = attr.split('.')
    try:
        if parts[0] == 'self':
            res = advance(obj, parts[1:])
            if res in base_types:
                return res
            return 'object'
        elif event and event in event_vbls and parts[0] in event_vbls[event]:
            t = event_vbls[event][parts[0]]
            if t == 'object' and event == 'collide' and event_sub:
                t = event_sub
           res = advance(t, parts[1:])
           if res in base_types:
               return res
           return 'object'
        else:
            return advance(parts[0], parts[1:])
    except (IndexError, Object.DoesNotExist, Custom_Attr.DoesNotExist):
        return False

def advance(type, attrs):
    if not attrs: return type
    attr = attrs[0]
    if type in ('game', 'object'):
        return advance(methods[type][attr], attrs[1:])
    else:
        obj = Object.objects.get(title = type)
        if attr in methods['object']:
            return advance(methods['object'][attr], attrs[1:])
        cattr = obj.custom_attrs.get(name=attr)
        ctype = cattr.type
        if ctype == 'object':
            ctype = cattr.sub_type
        return advance(ctype, attrs[1:])

str_rx = re.compile("^'.+?'$")
int_rx = re.compile('^[0-9]+$')
float_rx = re.compile('^[0-9]*(?:\.[0-9]+)$')
bool_rx = re.compile('^true|false$')

def const_type(const):
    if str_rx.match(const):return 'str'
    if int_rx.match(const):return 'int'
    if float_rx.match(const):return 'float'
    if bool_rx.match(const):return 'bool'
    return False


def get_target(lang):
    if lang == 'haxe':
        return 'this'
    return 'self'

def conv_target(var, lang):
    if var.split('.')[0] == 'self':
        var = utils.get_target(lang) + '.'.join(var.split('.')[1:])
    return var

def export(value, lang):
    type, rest = value.split(':', 1)
    type = {'c':'const','p':'percent','f','func'}[type]
    if type == 'const':
        return const
    elif type == 'percent':
        num, var = rest.split(':')
        num = int(num)
        var = conv_target(var)
        return '0.%d * %s' % (num, var)
    elif type == 'func':
        fn, args = rest.split(':', 1)
        fn = conv_target(var)
        args = json.loads(args)
        return '%s(%s)' % (fn, ', '.join(export(arg) for arg in args))

# vim: et sw=4 sts=4
