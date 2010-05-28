#!/usr/bin/env python

import json

jq = window.jQuery

loading = False

def post(command, data, callback):
    global loading

    def meta(text, status, request):
        global loading
        loading = False
        data = dict(json.loads(text))

        if data['error'] is not None:
            mb = window.Ext.MessageBox
            js.mb.alert('Congradulations!', 'You found a bug! Maybe.')
            js.mb.setIcon(mb.ERROR)
            
        callback(data)
        if not loading:
            js.jq('#loading-icon').hide()

    def onerror(request, text, error):
        error = definedor(error, '')
        if text == 'timeout':
            message = 'Couldn\'t reach the server. Check your internet connection and/or try again later. Sorry.' + str(error)
        else:
            message = 'Sorry, a server error occurred. Please reload the page and try again. ' + str(error)
        mb = window.Ext.MessageBox
        def doreload(*a):
            window.location.reload()
        js.mb.alert('Error', message, doreload)
        js.mb.setIcon(mb.ERROR)
        
    onerror._accept_undefined = True

    js.jq.ajax({
        'cache': False,
        'data': {'data':json.dumps(data)},
        'dataType': 'text',
        'error': onerror,
        'success': meta,
        'type': 'POST',
        'url': '/editor/ajax/' + command + '/',
    })



    # js.jq.post('/editor/ajax/' + command, data, callback, 'text')
    loading = True
    js.jq('#loading-icon').show()
    print 'yeah'


# vim: et sw=4 sts=4
