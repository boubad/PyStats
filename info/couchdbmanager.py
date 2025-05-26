import couchdb2
import sys
from info import key_doctype, key_id, key_rev, key_attachments, key_docs


class CouchDBManager(object):
    """class CouchDBManager"""

    def __init__(
        self,
        dburl: str = "http://boubad:bouba256@services.diarra.ovh:5984/",
        username: str = "boubad",
        password: str = "bouba256",
        dbname: str = "dbtest"
    ) -> None:
        # self._server = None
        # self._db = None
        self._serverurl = None
        self._dbname = None
        if len(dburl) > 0:
            try:
                xurl = dburl.strip()
                if len(xurl) > 0:
                    if not xurl.endswith("/"):
                        xurl += "/"
                    if not xurl.startswith("http://") and not xurl.startswith(
                        "https://"
                    ):
                        xurl = "http://" + dburl
                    self._server = couchdb2.Server(
                        href=xurl, username=username, password=password
                    )
                    self._serverurl = xurl
                    if len(dbname) > 0:
                        sname = dbname.strip().lower()
                        if len(sname) > 0 and sname in self._server:
                            self._db = self._server[sname]
                            self._dbname = sname
            except:  # noqa: E722
                pass

    @property
    def base_url(self) -> str | None:
        return self._serverurl

    @property
    def database_name(self) -> str | None:
        return self._dbname

    @database_name.setter
    def database_name(self, s: str) -> None:
        if s is None:
            return
        ss = s.strip().lower()
        if len(ss) < 1:
            return
        if self._server is not None and ss in self._server:
            self._db = self._server[ss]
            self._dbname = ss

    @property
    def database(self) -> couchdb2.Database | None:
        return self._db

    @property
    def server(self) -> couchdb2.Server | None:
        return self._server

    @property
    def is_online(self) -> bool:
        return self._server.up()
        
    @property
    def valid(self) -> bool:
        return self.is_online

    def get_docs(
        self, selector: dict, skip: int = 0, count: int = 128, fields: list | None = None
    ) -> list:
        docs = self._db.find(selector=selector, limit=count, skip=skip, fields=fields)
        return docs[key_docs]

    def get_docs_count(self, selector: dict) -> int:
        xdocs = self._db.find(
            selector=selector, skip=0, limit=sys.maxsize, fields=[key_id]
        )
        return len(xdocs[key_docs])

    def get_docs_by_type(
        self, stype: str, skip: int = 0, count: int = 128, fields: list | None = None
    ) -> list:
        selector = {key_doctype: stype}
        return self.get_docs(selector, skip, count, fields)

    def get_doc_by_selector(self, sel: dict) -> dict | None:
        xdocs = self._db.find(selector=sel, limit=1, skip=0)
        docs = xdocs[key_docs]
        if len(docs) > 0:
            return docs[0]
        return None

    def get_doc_by_id(self, docid: str) -> dict | None:
        if docid in self._db:
            return self._db[docid]
        return None

    def remove_doc_by_id(self, docid: str) -> None:
        if docid in self._db:
            doc = self._db[docid]
            self._db.delete(doc)

    def maintains_doc(self, rdoc: dict, sels: list | None = None) -> dict | None:
        doc: dict = {}
        if rdoc is None:
            return None
        if isinstance(rdoc, dict):
            for key, value in rdoc.items():
                if value is not None:
                    xkey: str = key
                    if xkey.startswith("_"):
                        if xkey == key_id:
                            doc[key_id] = value
                    else:
                        doc[key] = value
        else:
            for key, value in rdoc.__dict__.items():
                if value is not None:
                    xkey: str = key
                    if xkey.startswith("_"):
                        if xkey == key_id:
                            doc[key_id] = value
                    else:
                        doc[key] = value
        if len(doc) < 1:
            return None
        docid: str | None = None
        rev: str | None = None
        old_doc: dict | None = None
        if key_id in doc:
            sid = doc[key_id]
            if sid in self._db:
                old_doc = self._db[sid]
                docid = old_doc[key_id] # type: ignore
                rev = old_doc[key_rev] # type: ignore
            else:
                docid = sid
        if sels is not None:
            if len(sels) > 0:
                for sel in sels:
                    xdocs = self._db.find(selector=sel, limit=1, skip=0)
                    docs = xdocs[key_docs]
                    if len(docs) > 0:
                        old_doc = docs[0]
                        docid = old_doc[key_id] # type: ignore
                        rev = old_doc[key_rev] # type: ignore
        if old_doc is not None:
            if key_attachments in old_doc:
                doc[key_attachments] = old_doc[key_attachments]
        if docid is not None and len(docid) > 0:
            doc[key_id] = docid
        if rev is not None and len(rev) > 0:
            doc[key_rev] = rev
        self._db.put(doc)
        return doc
