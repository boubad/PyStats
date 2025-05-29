from info.baseobject import BaseObject
from info import doctype_statitem, key_datasetid, key_index, key_name, key_data


class StatItemObject(BaseObject):
    def __init__(self, the_dict: dict = None):
        super().__init__(the_dict=the_dict, the_doctype=doctype_statitem)

    @property
    def datasetid(self) -> str | None:
        if key_datasetid not in self:
            return None
        return self[key_datasetid]

    @datasetid.setter
    def datasetid(self, s: str):
        if s is not None:
            ss = s.strip()
            if len(ss) == 0:
                self[key_datasetid] = None
            else:
                self[key_datasetid] = ss
        else:
            self[key_datasetid] = None

    @property
    def index(self) -> int | None:
        if key_index not in self:
            return None
        return self[key_index]

    @index.setter
    def index(self, i: int):
        if i is not None:
            self[key_index] = int(i)
        else:
            self[key_index] = None

    @property
    def name(self) -> str | None:
        if key_name not in self:
            return None
        return self[key_name]

    @name.setter
    def name(self, s: str):
        if s is not None:
            ss = s.strip()
            if len(ss) == 0:
                self[key_name] = None
            else:
                self[key_name] = ss
        else:
            self[key_name] = None

    @property
    def data(self) -> dict | None:
        if key_data not in self:
            return None
        return self[key_data]

    @data.setter
    def data(self, d: dict):
        if d is not None:
            if isinstance(d, dict):
                self[key_data] = d
            else:
                raise ValueError("Data must be a dictionary.")
        else:
            self[key_data] = None

    @property
    def persist_map(self) -> dict:
        d = super().persist_map
        if self.datasetid is not None:
            d[key_datasetid] = self.datasetid
        if self.index is not None:
            d[key_index] = self.index
        if self.name is not None:
            d[key_name] = self.name
        if self.data is not None:
            d[key_data] = self.data
        return d

    @property
    def is_valid(self) -> bool:
        return super().is_valid and self.datasetid is not None and self.name is not None
