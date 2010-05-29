#!/usr/bin/env python

mb = window.Ext.MessageBox

class ProgressBar:
    def __init__(self, title, message):
        js.mb.progress(title, message)

    def update(self, amount, text=None):
        if text is None:
            text = str(round(amount*100)) + '% completed'
        js.mb.updateProgress(amount, text)

    def setMessage(self, message):
        js.mb.updateText(message)

    def done(self):
        js.mb.hide()

class NumProgressBar(ProgressBar):
    def __init__(self, title, message, total):
        ProgressBar.__init__(self, title, message)
        self.total = float(total)
        self.completed = 0

    def increment(self, message = None):
        self.completed += 1
        self.update(self.completed/self.total, message)

# vim: et sw=4 sts=4
