from sqlalchemy import null

from .device_event import *


class DeviceEventLogin(DeviceEvent):
    __tablename__ = 'device_event_login'
    event_id = Column(Integer, ForeignKey('device_event.id'), primary_key=True)
    # 登录事件
    username = Column(String(255), nullable=True, comment='登录用户名')
    login_purpose = Column(String(255), nullable=True, comment='登录目的')

    __mapper_args__ = {
        'polymorphic_identity': 'device_event_login',
    }
