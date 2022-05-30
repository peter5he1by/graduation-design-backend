from .base import *


class DeviceVersion(Base, BaseModel):
    __tablename__ = 'device_version'
    code_name = Column(String(255), nullable=True)
    internal_version = Column(Integer, nullable=False, index=True)
    external_version = Column(String(255), nullable=True)
    file_url = Column(Text, nullable=False)
    hash_value = Column(String(255), nullable=False)
