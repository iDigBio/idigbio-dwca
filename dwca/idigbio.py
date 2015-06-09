class Records:
    # Core type -> lookup_function, returning the coreid
    __relations = {
        "records": lambda r: r["_id"],
        "mediarecords": lambda r: r["_source"]["mediarecords"][0],
        "unique.locality": lambda r: identify_locality(r["_source"]["locality"]),
        "unique.scientificname": lambda r: identify_locality(r["_source"]["scientificname"])
    }
    type_name = "records"
    type_xml = "http://rs.tdwg.org/dwc/terms/Occurrence"

    def __init__(self,core=True,core_type=None):
        if core:
            self.id_field = "id"
            self.myid_field = None
            self.myid_func = lambda r: r["_id"]
        else:
            self.id_field = "coreid"
            self.myid_field = "idigbio:uuid"
            self.myid_func = lambda r: r["_id"]

        if core_type is None or core:
            self.id_func = self.myid_func
        elif core_type.type_name in self.__relations:
            self.id_func = self.__relations[core_type.type_name]
        else:
            raise NotImplementedError

class MediaRecords:
    # Core type -> lookup_function, returning the coreid
    __relations = {
        "mediarecords": lambda r:["_id"],
        "records": lambda r: r["_source"]["records"][0],
        "unique.locality": lambda r: identify_locality(r["_source"]["inner_hits"][0]["locality"]),
        "unique.scientificname": lambda r: identify_locality(r["_source"]["inner_hits"][0]["scientificname"])
    }
    type_name = "mediarecords"
    type_xml =  "http://rs.tdwg.org/ac/terms/Multimedia"

    def __init__(self,core=True,core_type=None):
        if core:
            self.id_field = "id"
            self.myid_field = None
            self.myid_func = lambda r: r["_id"]
        else:
            self.id_field = "coreid"
            self.myid_field = "idigbio:uuid"
            self.myid_func = lambda r: r["_id"]

        if core_type is None or core:
            self.id_func = self.myid_func
        elif core_type.type_name in self.__relations:
            self.id_func = self.__relations[core_type.type_name]
        else:
            raise NotImplementedError