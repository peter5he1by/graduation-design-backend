from .base import *


class DeviceLog(Base, BaseModel):
    __tablename__ = 'device_log'
    device_id = Column(Integer, ForeignKey('device.id'))
    content = Column(LONGTEXT)
    start_time = Column(DateTime())
    end_time = Column(DateTime())

    device = relationship('Device')

    def __json__(self) -> dict:
        ret = super().__json__()
        ret.pop('content')
        ret.setdefault('size', len(self.content))
        return ret
