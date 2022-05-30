from .base import *


class DeviceDataTemperature(Base, BaseModel):
    __tablename__ = 'device_data_temperature'
    device_id = Column(Integer, ForeignKey('device.id'))
    time = Column(DateTime())
    data = Column(Float)
