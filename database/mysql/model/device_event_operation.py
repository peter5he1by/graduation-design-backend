from sqlalchemy import null

from .device_event import *


class DeviceEventOperation(DeviceEvent):
    __tablename__ = 'device_event_operation'
    event_id = Column(Integer, ForeignKey('device_event.id'), primary_key=True)
    # 登录事件
    username = Column(String(255), nullable=True, comment='操作用户')
    operation_type = Column(String(255), nullable=False, comment='操作类型')
    detail = Column(Text, nullable=True, comment="详细数据")
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }
