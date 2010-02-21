
class Asset:
    def __init__(self, parent, name, info):
        self.parent = parent
        self.name = name
        self.info = info

    def inline_output(self):
        return json.dumps(self.info)

    def output(self):
        return ''


    




