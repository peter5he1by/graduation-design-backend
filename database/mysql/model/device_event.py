from .base import *


class DeviceEvent(Base, BaseModel):
    __tablename__ = 'device_event'
    device_id = Column(Integer, ForeignKey('device.id'))
    type = Column(String(64))

    device = relationship('Device')

    __mapper_args__ = {
        'polymorphic_identity': 'device_event',
        'polymorphic_on'      : type
    }
