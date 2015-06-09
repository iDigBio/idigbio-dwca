import uuid

class Archive:
    def __init__(self,name=None):
        if name is None:
            self.name = str(uuid.uuid4())
        else:
            self.name = name

        self.files = []

    def new_file(self,t,fields,core=True):
        r = RecordFile(core=core, t=t, fields=fields)
        self.files.append(r)
        return r

class RecordFile:

    def __init__(self, core=True, t="occurence", fields=[]):
        self.core = core
        self.type = t
        self.fields = fields





