from datetime import datetime

import humps
from sqlalchemy import (Column, ForeignKey, Integer, String, Text, text, DateTime, func, desc, TIMESTAMP, case, Float)
from sqlalchemy.orm import (declarative_base, relationship, backref, immediateload)
import json_fix
from sqlalchemy.dialects.mysql import LONGTEXT

from main import db_engine

Base = declarative_base(db_engine)


class BaseModel:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), server_default=func.NOW())
    updated_at = Column(DateTime(), server_default=func.NOW(), server_onupdate=func.NOW())

    def __json__(self) -> dict:
        ret = self.__dict__.copy()
        ret.pop('_sa_instance_state', None)
        return humps.camelize(ret)
