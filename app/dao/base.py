from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from typing import Any
from bson import ObjectId
from fastapi import Depends
from app.models.base import MongoModel, StudentInDB
from app.models.bill import BillInDB, ReceiptInDB


def get_collection(request: Request, collection):
    return request.app.database[collection]


def get_db(request: Request) -> MongoClient:
    return request.app.database


class BaseRepository:
    def __init__(self, collection, key_field="_id", mongo_model_class=None):
        self.key_field = key_field
        self.collection = collection
        self.mongo_model_class = mongo_model_class

    def all(self):
        return [self.to_model(item) for item in self.collection.find()]

    def get(self, key: Any):
        if self.key_field == "_id":
            if isinstance(key, str):
                key = ObjectId(key)
        obj = self.collection.find_one({self.key_field: key})
        if obj:
            return self.to_model(obj)

    def delete(self, key: Any):
        del_res = self.collection.delete_one({self.key_field: key})
        return del_res.acknowledged and del_res.deleted_count == 1

    def delete_all(self, query: dict):
        del_res = self.collection.delete(query)
        return del_res.acknowledged and del_res.deleted_count > 0

    def find(self, find: dict):
        return [self.to_model(item) for item in self.collection.find(find)]

    def find_one(self, find: dict):
        obj = self.collection.find_one(find)
        if obj:
            return self.to_model(obj)

    def insert_one(self, obj: Any):
        insert_res = self.collection.insert_one(obj)
        if insert_res.acknowledged:
            return insert_res.inserted_id

    def insert(self, arr: list[Any]):
        insert_res = self.collection.insert_many(arr)
        if insert_res.acknowledged:
            return insert_res.inserted_ids

    def update_one(self, key: str, obj: Any):
        update_res = self.collection.update_one(
            {self.key_field: key}, {"$set": jsonable_encoder(obj)}
        )
        return update_res.acknowledged and update_res.matched_count == 1

    def delete_many(self, query):
        delete_res = self.collection.delete_many(query)
        if delete_res.acknowledged:
            return delete_res.deleted_count

    def delete(self, key):
        delete_res = self.collection.delete_one({self.key_field: key})
        return delete_res.acknowledged and delete_res.deleted_count == 1

    def to_model(self, data):
        if self.mongo_model_class:
            return self.mongo_model_class(**data)
        return data

    def to_dict(self, model):
        if isinstance(model, MongoModel):
            return model.dict()
        return model


def get_student_repo(db=Depends(get_db)) -> BaseRepository:
    return BaseRepository(
        db["students"], "enrollmentNumber", mongo_model_class=StudentInDB
    )


def get_bill_repo(db=Depends(get_db)) -> BaseRepository:
    return BaseRepository(db["bills"], mongo_model_class=BillInDB)


def get_receipt_repo(db=Depends(get_db)) -> BaseRepository:
    return BaseRepository(db["receipts"], mongo_model_class=ReceiptInDB)
