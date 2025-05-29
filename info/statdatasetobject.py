from info.baseobject import BaseObject
from info import doctype_dataset, key_name, key_sigle


class StatItemObject(BaseObject):
    def __init__(self, the_dict: dict = None):
        super().__init__(the_dict=the_dict, the_doctype=doctype_dataset)

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
    def sigle(self) -> str | None:
        if key_sigle not in self:
            return None
        return self[key_sigle]

    @sigle.setter
    def sigle(self, s: str):
        if s is not None:
            ss = s.strip()
            if len(ss) == 0:
                self[key_sigle] = None
            else:
                self[key_sigle] = ss
        else:
            self[key_sigle] = None

    @property
    def persist_map(self) -> dict:
        d = super().persist_map
        if self.sigle is not None:
            d[key_sigle] = self.sigle
        if self.name is not None:
            d[key_name] = self.name
        return d

    @property
    def is_valid(self) -> bool:
        return (
            super().is_valid
            and self.name is not None
            and self.sigle is not None
            and len(self.name) > 0
            and len(self.sigle) > 0
        )
