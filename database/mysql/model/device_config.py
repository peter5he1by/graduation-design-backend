from .base import *


class DeviceConfig(Base, BaseModel):
    __tablename__ = 'device_config'
    device_id = Column(Integer, ForeignKey('device.id'))
    content = Column(Text)
    type = Column(String(255), nullable=True)

    device = relationship('Device')
