from . import _type,_pyctyerror
import pprint

class array(_type.CType, list):
    def __init__(self,value : list, dtype : type):
        self.value = value
        self.dtype = dtype
        for i in value:
            if not type(i) == dtype:
                raise _pyctyerror.PyCTYError("Object Type Must Be Type In dtype")
    def __str__(self):
        return pprint.PrettyPrinter(indent=4).pformat(f"array({self.value},dtype={str(self.dtype)})")

    def __getitem__(self, item):
         return self.value[item]

    def __setitem__(self,index,value):
         self.value[index] = value