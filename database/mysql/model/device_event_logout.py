from .device_event import *


class DeviceEventLogout(DeviceEvent):
    __tablename__ = 'device_event_logout'
    event_id = Column(Integer, ForeignKey('device_event.id'), primary_key=True)
    # 注销事件
    username = Column(String(255), nullable=True, comment='注销的用户名')
    work_contents = Column(Text, nullable=True, comment='工作内容')

    __mapper_args__ = {
        'polymorphic_identity': 'device_event_logout',
    }
