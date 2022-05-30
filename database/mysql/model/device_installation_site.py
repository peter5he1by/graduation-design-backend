from .base import *


class DeviceInstallationSite(Base, BaseModel):
    __tablename__ = 'device_installation_site'
    id = BaseModel.id
    pid = Column(Integer, ForeignKey('device_installation_site.id'))  # , server_default=text('NULL'))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    devices = relationship('Device', back_populates='installation_site')
    parent_installation_site = relationship('DeviceInstallationSite', remote_side=[id])
    sub_installation_sites = relationship(
        'DeviceInstallationSite', back_populates='parent_installation_site', lazy='immediate'
    )  # ont-to-many relations

    def __json__(self) -> dict:
        ret = super().__json__()
        if ret['pid'] is None:
            ret['pid'] = 0
        return ret
