from .base import *


class Device(Base, BaseModel):
    __tablename__ = 'device'
    uuid = Column(String(255), nullable=False, unique=True)
    secret_key = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    installation_site_id = Column(Integer, ForeignKey('device_installation_site.id'))

    installation_site = relationship('DeviceInstallationSite', back_populates='devices', lazy='immediate')
    device_info = relationship('DeviceInfo', back_populates='device', order_by=desc(text('created_at')),
                               uselist=False, lazy='immediate')
    events = relationship('DeviceEvent', back_populates='device')
