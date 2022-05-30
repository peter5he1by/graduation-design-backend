from .device_event import *


class DeviceEventStatusChange(DeviceEvent):
    __tablename__ = 'device_event_status_change'
    event_id = Column(Integer, ForeignKey('device_event.id'), primary_key=True)
    # 状态变更事件
    status = Column(Integer, nullable=False, comment='状态')

    event = relationship('DeviceEvent')

    __mapper_args__ = {
        'polymorphic_identity': 'device_event_status_change',
    }
