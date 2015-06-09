import unicodecsv

try:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
except ImportError:
    from io import StringIO

from fieldnames import get_canonical_name,types

from log import logger as global_logger

class MissingFieldsException(Exception):
    def __init__(self,name,lineNumber,fieldnum,fieldname,lineArr):
        message = """
    File: {0}, Line: {1}
    Field Number: {2}, Field Key: {3}
    Line Array: {4}, Length: {5}
""".format(name,lineNumber,fieldnum,fieldname,repr(lineArr),len(lineArr))
        super(MissingFieldsException,self).__init__(message)

class line_lengthException(Exception):
    def __init__(self,name,lineNumber,line_length,lineArr):
        message = """
    File: {0}, Line: {1}
    Expected Line Length: {2}, Actual Line Length: {4}
    Line Array: {3}
""".format(name,lineNumber,line_length,repr(lineArr),len(lineArr))

class DelimitedFileReader:
    def __init__(self,filename,header=None,tabs=False,encoding="utf-8",logger=None):
        if logger is None:
            self.logger = global_logger
        else:
            self.logger = logger

        dialect = unicodecsv.excel
        if tabs:
            dialect = unicodecsv.excel_tab
            if not self.filename.endswith(".tsv"):
                self.filename = filename + ".tsv"
        else:
            if not self.filename.endswith(".csv"):
                self.filename = filename + ".csv"


        self.__filehandle = open(self.filename,"rb")
        self._reader = unicodecsv.reader(self.__filehandle, encoding=encoding, dialect=dialect)
        if header is None:
            self.header = {}
            h = self._reader.next()
            for i, f in enumerate(h):
                cn = get_canonical_name(f)
                if cn[0] is not None:
                    self.header[i] = cn[0]
        else:
            self.header = header
        self.line_length = len(self.header)

    def __iter__(self):
        """
            Returns the object itself, as per spec.
        """        
        return self

    def close(self):
        self.__filehandle.close()

    def next(self):
        return self.readline()

    def readline(self,size=None):
        lineDict = None
        while lineDict is None:     
            try:                
                lineArr = self._reader.next()
                self.lineCount += 1
                if self.line_length is None:
                    self.line_length = len(lineArr)
                elif self.line_length != len(lineArr):
                    raise line_lengthException(self.name,self.lineCount,self.line_length,lineArr)
                
                lineDict = {}
                for k in self.header:
                    try:
                        lineArr[k] = lineArr[k].strip()
                        if lineArr[k] != "":
                            lineDict[self.header[k]] = lineArr[k]
                    except IndexError as e:                        
                        raise MissingFieldsException(self.name,self.lineCount,k,self.fields[k],lineArr)
                return lineDict
            except UnicodeDecodeError:
                lineDict = None
                self.lineCount += 1
                self.logger.warn("Unicode Decode Exception: {0} Line {1}".format(self.name,self.lineCount))
                self.logger.debug(traceback.format_exc())                
            except MissingFieldsException:
                lineDict = None
                self.logger.warn("Missing Fields Exception: {0} Line {1}".format(self.name,self.lineCount))
                self.logger.debug(lineArr)
                self.logger.debug(traceback.format_exc())
            except line_lengthException:
                lineDict = None
                self.logger.warn("line_lengthException: {0} Line {1} ({2},{3})".format(self.name,self.lineCount,self.line_length,len(lineArr)))
                self.logger.debug(lineArr)
                self.logger.debug(traceback.format_exc())

class DelimitedFileWriter:

    def __init__(self,filename,header,tabs=False,encoding="utf-8",use_string_io=False,logger=None):
        dialect = unicodecsv.excel
        if tabs:
            dialect = unicodecsv.excel_Tab
            self.filename = filename + ".tsv"
        else:
            self.filename = filename + ".csv"

        if use_string_io:
            self.__filehandle = StringIO()
        else:
            self.__filehandle = open(self.filename,"wb")

        self._writer = unicodecsv.writer(self.__filehandle,encoding=encoding,dialect=dialect)
        self.header_array = []
        for k in sorted(header.keys())
            self.header_array.push(header[k])
        self._writer.writerow(self.header_array)

    def write(self,d):
        fa = []
        for k in self.header_array:
            if k in d:
                fa.append(d[k])
            else:
                fa.append("")
        self._writer.writerow(fa)
