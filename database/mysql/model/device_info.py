from .base import *


class DeviceInfo(Base, BaseModel):
    __tablename__ = 'device_info'
    device_id = Column(Integer, ForeignKey('device.id'))
    software_info = Column(String(255))
    hardware_info = Column(String(255))
    remark = Column(Text)

    device = relationship('Device', back_populates='device_info')
