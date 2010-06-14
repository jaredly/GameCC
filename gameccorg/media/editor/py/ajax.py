
from restive_js.ext_client import ExtClient
ajax = ExtClient('/editor/ajax/')

def ajax_start():
    window.jQuery('#loading-icon').show()

def ajax_end():
    if not ajax.loading:
        window.jQuery('#loading-icon').hide()

ajax.listeners['start'].append(ajax_start)
ajax.listeners['end'].append(ajax_end)

# vim: et sw=4 sts=4
