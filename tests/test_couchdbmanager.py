import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import unittest
from info import couchdbmanager
from tests.fixture import TestFixture


class CouchDBManagerTestCase(unittest.TestCase):
    dburl: str = TestFixture().db_url
    dbname: str = TestFixture().db_name

    def test_constructor(self):
        man = couchdbmanager.CouchDBManager(dbname=self.dbname, dburl=self.dburl)
        b = man.is_online
        self.assertTrue(b)
        xurl = "services.diarra.ovh:5984"
        xman = couchdbmanager.CouchDBManager(dbname=self.dbname, dburl=xurl)
        xb = xman.valid
        self.assertTrue(xb)

    def test_isonline(self):
        man = couchdbmanager.CouchDBManager(dbname=self.dbname, dburl=self.dburl)
        b = man.is_online
        self.assertTrue(b)

    def test_checkindexes(self):
        man = couchdbmanager.CouchDBManager(dbname=self.dbname, dburl=self.dburl)
        b = man.is_online
        self.assertTrue(b)
        indexes =[
            ["doctype"],
            ["setname"],
            ["status"],
            ["doctype", "setname"],
            ["doctype", "status"],
            ["doctype", "setname", "status"],
        ]
        db = man.database
        for index in indexes:
            d= db.put_index(index) # type: ignore
            print("\nINDEX: {}\n".format(d))
            
    def test_getdocscount(self):
        selector = {"doctype": "etud"}
        man = couchdbmanager.CouchDBManager(dbname=self.dbname, dburl=self.dburl)
        b = man.is_online
        self.assertTrue(b)
        n = man.get_docs_count(selector)
        self.assertTrue(n >= 0)

    def test_getdocs(self):
        skip = 0
        limit = 5
        stype = "etud"
        man = couchdbmanager.CouchDBManager(dbname=self.dbname, dburl=self.dburl)
        b = man.is_online
        self.assertTrue(b)
        docs = man.get_docs_by_type(stype, skip, limit)
        n = len(docs)
        if n > 0:
            self.assertEqual(limit, n)
            key_id = "_id"
            key_rev = "_rev"
            for doc in docs:
                b = key_id in doc
                self.assertTrue(b)
                docid = doc[key_id]
                b = key_rev in doc
                self.assertTrue(b)
                xdoc = man.get_doc_by_id(docid)
                b = key_id in xdoc # type: ignore
                self.assertTrue(b)
                xid = xdoc[key_id] # type: ignore
                self.assertEqual(docid, xid)


if __name__ == "__main__":
    unittest.main()
