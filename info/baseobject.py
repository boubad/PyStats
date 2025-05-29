from info import key_id, key_status, key_doctype, key_rev, key_attachments
from info.statitemstatustype import StatItemStatusType


class BaseObject(dict):
    def __init__(self, the_dict: dict = None, the_doctype: str = None):
        super().__init__()
        if the_dict is not None:
            if isinstance(the_dict, dict):
                self.update(the_dict)
        if the_doctype not in (None, ""):
            self[key_doctype] = the_doctype

    @property
    def doctype(self) -> str | None:
        if key_doctype not in self:
            return None
        return self[key_doctype]

    @doctype.setter
    def doctype(self, s: str):
        if s is not None:
            self[key_doctype] = s.strip()
        else:
            self[key_doctype] = None

    @property
    def id(self) -> str | None:
        if key_id not in self:
            return None
        return self[key_id]

    @id.setter
    def id(self, s: str):
        if s is not None:
            ss = s.strip()
            if len(ss) == 0:
                self[key_id] = None
            else:
                self[key_id] = ss
        else:
            self[key_id] = None

    @property
    def status(self) -> StatItemStatusType | None:
        if key_status not in self:
            return None
        s = self[key_status]
        if isinstance(s, StatItemStatusType):
            return s
        elif isinstance(s, int):
            return StatItemStatusType(s)
        else:
            raise ValueError(f"Invalid status type: {s}")

    @status.setter
    def status(self, s: StatItemStatusType | None):
        if s is None:
            self[key_status] = None
        elif isinstance(s, StatItemStatusType):
            self[key_status] = s
        elif isinstance(s, int):
            self[key_status] = StatItemStatusType(s)
        else:
            raise ValueError(f"Invalid status type: {s}")

    @property
    def rev(self) -> str | None:
        if key_rev not in self:
            return None
        return self[key_rev]

    @rev.setter
    def rev(self, s: str):
        if s is not None:
            ss = s.strip()
            if len(ss) == 0:
                self[key_rev] = None
            else:
                self[key_rev] = ss
        else:
            self[key_rev] = None

    @property
    def attachments(self) -> dict | None:
        if key_attachments not in self:
            return None
        return self[key_attachments]

    @attachments.setter
    def attachments(self, s: dict | None):
        if s is None:
            self[key_attachments] = None
        elif isinstance(s, dict):
            self[key_attachments] = s
        else:
            raise ValueError(f"Attachments must be a dictionary, got {type(s)}")

    @property
    def persist_map(self) -> dict:
        vret = dict()
        if self.id is not None and len(self.id) > 0:
            vret[key_id] = self.id
        if self.doctype is not None and len(self.doctype) > 0:
            vret[key_doctype] = self.doctype
        if self.status is not None:
            vret[key_status] = self.status
        return vret

    @property
    def is_valid(self) -> bool:
        return self.doctype is not None and len(self.doctype) > 0
