import uuid

class GenericFile:

    # Core type -> lookup_function, returning the coreid
    __relations = {        
    }
    type_name = "dataset"
    type_xml = "http://purl.org/dc/dcmitype/Dataset"

    def __init__(self,core=True,core_type=None):
        if core_type is None or core:
            self.id_field = "id"
            self.myid_field = None
            self.myid_func = lambda r: r["id"]
        elif not core and core_type is not None:
            self.id_field = "coreid"
            self.myid_field = None
            self.myid_func = None

        if core_type is None or core:
            self.id_func = self.myid_func
        elif core_type.type_name in self.__relations:
            self.id_func = self.__relations[core_type]
        else:
            self.id_func = lambda r: r["coreid"]

class Archive:
    def __init__(self,name=None):
        if name is None:
            self.name = str(uuid.uuid4())
        else:
            self.name = name

        self.files = []
        self.core_type = None

    def new_file(self,t,fields):
        core = False
        if self.core_type is None:
            self.core_type = t
            core = True

        r = RecordFile(core=core, t=t, core_type=self.core_type, fields=fields)
        self.files.append(r)
        return r

    def __repr__(self):
        return "< " + self.name + ":\n\t" + "\n\t".join([repr(f) for f in self.files]) + "\n>"

class RecordFile:

    def __init__(self, core=True, t=GenericFile, core_type=None, fields=[]):
        self.core = core
        self.t = t(core=core, core_type=core_type)
        self.fields = fields


    def __repr__(self):
        other_fields = [self.t.id_field]
        if self.t.myid_field is not None:
            other_fields.append(self.t.myid_field)
        return "< " + self.t.type_name + ": " + ",".join(other_fields + self.fields) + " >"

def main():
    from .idigbio import Records, MediaRecords
    dwca = Archive()
    dwca.new_file(Records,["dwc:scientificName","dwc:locality"])
    dwca.new_file(MediaRecords,["ac:accessURI","dcterms:identifier"])

    print dwca

if __name__ == '__main__':
    main()




