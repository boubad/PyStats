from info.basemanager import BaseManager
from info import (
    doctype_dataset,
    doctype_statitem,
    key_id,
    key_datasetid,
    key_name,
    key_sigle,
    key_doctype,
)
from info.statdatasetobject import StatDatasetObject
from info.statitemobject import StatItemObject
import pandas as pd
import numpy as np


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

    def import_from_dataframe(
        self, df: pd.DataFrame, datasetname: str, indexcol: str = None
    ) -> bool:
        if df is None or df.empty:
            return False
        if datasetname is None or len(datasetname) == 0:
            return False
        colnames = df.columns.to_list()
        dataset = self.find_dataset_by_name(datasetname)
        if dataset is None:
            dataset = StatDatasetObject()
            dataset.name = datasetname
            dataset.sigle = datasetname.lower().replace(" ", "_")
            dataset.variables = colnames
            dataset.observations = "Imported from DataFrame"
            dataset = self.maintains_dataset(dataset)
            if dataset is None:
                return False
        datasetid = dataset.id
        if datasetid is None:
            return False
        nrows, ncols = df.shape
        itemsnames = None
        if indexcol is not None and indexcol in df.columns:
            itemsnames = df[indexcol].tolist()
        else:
            xinds = df.index.to_list()
            for i in range(nrows):
                if itemsnames is None:
                    itemsnames = []
                ss = str(xinds[i])
                itemsnames.append(ss)
        for i in range(nrows):
            itemname = itemsnames[i]
            olditem = self.find_dataset_item_by_name(datasetid, itemname)
            if olditem is not None:
                continue
            idata = dict()
            for j in range(ncols):
                v = df.iloc[i, j]
                if v is None:
                    continue
                if pd.isnull(v):
                    continue
                if isinstance(v, str):
                    v = v.strip()
                    if len(v) == 0:
                        continue
                colname = colnames[j]
                idata[colname] = v
            if len(idata) == 0:
                continue
            item = StatItemObject()
            item.datasetid = datasetid
            item.name = itemname
            item.data = idata
            item = self.maintains_dataset_item(item)
            if item is None:
                return False
        return True

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
        r = man.get_doc_by_selector(selector)
        if r is None:
            return None
        return StatDatasetObject(r)

    def find_dataset_by_sigle(self, sigle: str) -> StatDatasetObject | None:
        selector = {key_doctype: doctype_dataset, key_sigle: sigle}
        man = self.manager
        r = man.get_doc_by_selector(selector)
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

    def delete_dataset(self, datasetid: str) -> bool:
        man = self.manager
        dataset = self.find_dataset_by_id(datasetid)
        if dataset is None:
            return False
        skip = 0
        count = 128
        done = False
        while not done:
            items = self.get_dataset_items(datasetid, skip, count, fields=[key_id])
            nitems = len(items)
            if nitems > 0:
                for item in items:
                    man.remove_doc_by_id(item.id)
            skip += nitems
            done = nitems < count
        man.remove_doc_by_id(datasetid)
        return True

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

    def maintains_dataset_item(self, item: StatItemObject) -> StatItemObject | None:
        if item is None or not item.is_valid:
            return None
        sels = []
        sels.append(
            {
                key_doctype: doctype_statitem,
                key_datasetid: item.datasetid,
                key_name: item.name,
            }
        )
        man = self.manager
        pdata = item.persist_map
        r = man.maintains_doc(pdata, sels=sels)
        if r is None:
            return None
        return StatItemObject(r)

    def find_dataset_item_by_name(
        self, datasetid: str, name: str
    ) -> StatItemObject | None:
        selector = {
            key_doctype: doctype_statitem,
            key_datasetid: datasetid,
            key_name: name,
        }
        man = self.manager
        r = man.find_doc_by_selector(selector)
        if r is None:
            return None
        return StatItemObject(r)

    def find_dataset_item_by_id(self, itemid: str) -> StatItemObject | None:
        man = self.manager
        r = man.find_doc_by_id(itemid)
        if r is None:
            return None
        return StatItemObject(r)
