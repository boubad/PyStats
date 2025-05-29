from info.couchdbmanager import CouchDBManager


class BaseManager(object):
    def __init__(
        self,
        dburl: str = "http://boubad:bouba256@services.diarra.ovh:5984/",
        username: str = "boubad",
        password: str = "bouba256",
        dbname: str = "dbtest",
    ):
        self._man = CouchDBManager(
            dburl=dburl, username=username, password=password, dbname=dbname
        )

    @property
    def manager(self) -> CouchDBManager:
        return self._man

    @property
    def is_online(self) -> bool:
        return self._man.is_online

    @property
    def valid(self) -> bool:
        return self.is_online
