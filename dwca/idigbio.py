class iDigBioObject:

    # Core type -> lookup_function, returning the coreid
    __relations = {        
    }

    def __init__(self,core=True,core_type=None):
        if core_type is None or core:
            self.id_field = "id"
            self.myid_field = None
            self.myid_func = lambda r: r["_id"]
        elif not core and core_type is not None:
            self.id_field = "coreid"
            self.myid_field = "idigbio:uuid"
            self.myid_func = lambda r: r["_id"]

        if core_type is None or core:
            self.id_func = self.myid_func
        if core_type in self.__relations:
            self.id_func = self.__relations[core_type]
        else:
            raise NotImplementedError

class Records(iDigBioObject):
    # Core type -> lookup_function, returning the coreid
    __relations = {
        "mediarecords": lambda r: r["_source"]["mediarecords"][0],
        "unique.locality": lambda r: identify_locality(r["_source"]["locality"]),
        "unique.scientificname": lambda r: identify_locality(r["_source"]["scientificname"])
    }

    def __init__(self,core=True,core_type=None):
        if core:
            self.id_field = "id"
            self.myid_field = None
            self.myid_func = lambda r: r["_id"]
        else:
            self.id_field = "coreid"
            self.myid_field = "idigbio:uuid"
            self.myid_func = lambda r: r["_id"]

        if core_type in self.__relations:
            self.id_func = self.__relations[core_type]
        else:
            raise NotImplementedError

class MediaRecords(iDigBioObject):
    # Core type -> lookup_function, returning the coreid
    __relations = {
        "records": lambda r: r["_source"]["records"][0],
        "unique.locality": lambda r: identify_locality(r["_source"]["inner_hits"][0]["locality"]),
        "unique.scientificname": lambda r: identify_locality(r["_source"]["inner_hits"][0]["scientificname"])
    }

    def __init__(self,core=True,core_type=None):
        if core:
            self.id_field = "id"
            self.myid_field = None
            self.myid_func = lambda r: r["_id"]
        else:
            self.id_field = "coreid"
            self.myid_field = "idigbio:uuid"
            self.myid_func = lambda r: r["_id"]

        if core_type in self.__relations:
            self.id_func = self.__relations[core_type]
        else:
            raise NotImplementedError