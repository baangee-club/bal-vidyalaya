from pydantic import BaseModel as PydanticBase, Extra
import datetime
from typing import Optional
from bson import ObjectId

class BaseModel(PydanticBase):
    class Config:
        json_encoders = {
            datetime.date: lambda dt: dt.isoformat(),
            datetime.datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

class OID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class MongoModel(BaseModel):
    def __init__(self, **data: dict):
        data = self._reformat_mongo_id_key(data)
        super(MongoModel, self).__init__(**data)

    class Config:
        # allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = Extra.forbid
        json_encoders = {
            ObjectId: str,
            datetime.date: lambda dt: dt.isoformat(),
            datetime.datetime: lambda dt: dt.isoformat(),
        }

    @staticmethod
    def _reformat_mongo_id_key(data):
        if not data:
            return data
        if "_id" in data and "id" not in data:
            data["id"] = data.pop("_id", None)
        return data


class Student(BaseModel):
    enrollmentNumber: str
    name: str
    startDate: datetime.date
    standard: str
    fees: int

class StudentInDB(MongoModel, Student):
    id: OID
