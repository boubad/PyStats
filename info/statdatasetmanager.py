from info.basemanager import BaseManager
from info import (
    doctype_dataset,
    doctype_statitem,
    key_data,
    key_datasetid,
    key_name,
    key_sigle,
    key_doctype,
)
from info.statdatasetobject import StatDatasetObject
from info.statitemobject import StatItemObject


class StatDatasetManager(BaseManager):
    def __init__(
        self,
        dburl: str = "http://boubad:bouba256@services.diarra.ovh:5984/",
        username: str = "boubad",
        password: str = "bouba256",
        dbname: str = "dbtest",
    ):
        super().__init__(
            dburl=dburl, username=username, password=password, dbname=dbname
        )

    def get_datasets_count(self) -> int:
        selector = {key_doctype: doctype_dataset}
        man = self.manager
        return man.get_docs_count(selector)

    def get_datasets(
        self, skip: int = 0, count: int = 128, fields: list = None
    ) -> list[StatDatasetObject]:
        selector = {key_doctype: doctype_dataset}
        vret = []
        man = self.manager
        rr = man.get_docs(selector, skip=skip, count=count, fields=fields)
        if rr is None:
            return vret
        for r in rr:
            if r is not None:
                vret.append(StatDatasetObject(r))
        return vret

    def find_dataset_by_name(self, name: str) -> StatDatasetObject | None:
        selector = {key_doctype: doctype_dataset, key_name: name}
        man = self.manager
        r = man.find_doc_by_selector(selector)
        if r is None:
            return None
        return StatDatasetObject(r)

    def get_dataset_by_sigle(self, sigle: str) -> StatDatasetObject | None:
        selector = {key_doctype: doctype_dataset, key_sigle: sigle}
        man = self.manager
        r = man.find_doc_by_selector(selector)
        if r is None:
            return None
        return StatDatasetObject(r)

    def find_dataset_by_id(self, datasetid: str) -> StatDatasetObject | None:
        man = self.manager
        r = man.get_doc_by_id(datasetid)
        if r is None:
            return None
        return StatDatasetObject(r)

    def maintains_dataset(self, dataset: StatDatasetObject) -> StatDatasetObject | None:
        if dataset is None or not dataset.is_valid:
            return None
        sels = []
        sels.append({key_doctype: doctype_dataset, key_sigle: dataset.sigle})
        sels.append({key_doctype: doctype_dataset, key_name: dataset.name})
        man = self.manager
        pdata = dataset.persist_map
        r = man.maintains_doc(pdata, sels=sels)
        if r is None:
            return None
        return StatDatasetObject(r)
    
    def _get_dataset_items_count(self, datasetid: str) -> int:
        selector = {
            key_doctype: doctype_statitem,
            key_datasetid: datasetid,
        }
        man = self.manager
        return man.get_docs_count(selector)
    
    def get_dataset_items(
        self,
        datasetid: str,
        skip: int = 0,
        count: int = 128,
        fields: list = None,
    ) -> list[StatItemObject]:
        selector = {
            key_doctype: doctype_statitem,
            key_datasetid: datasetid,
        }
        vret = []
        man = self.manager
        rr = man.get_docs(selector, skip=skip, count=count, fields=fields)
        if rr is None:
            return vret
        for r in rr:
            if r is not None:
                vret.append(StatItemObject(r))
        return vret
