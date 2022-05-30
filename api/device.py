import constant
from .common import *

bp = Blueprint('device', __name__, url_prefix='/device')

list_device_rules = {
    'installationSiteId': Rule(type=int, required=True)
}


@bp.route('/get_list', methods=['post'])
@pre.catch(list_device_rules)
def get_list(params):
    session = session_maker()
    inst_site_id = params['installationSiteId']
    if inst_site_id == 0:
        inst_site_id = None
    devices: List[Device]
    if inst_site_id is None:
        devices = session.execute(
            select(Device)
        ).scalars().all()
    else:
        devices = session.execute(
            select(Device)
                .where(Device.installation_site_id == inst_site_id)
        ).scalars().all()
    session.close()
    return resp(rst=devices)


add_device_rules = {
    'deviceName'        : Rule(type=str, required=True, gte=1, lte=100),
    'description'       : Rule(type=str, required=False),
    'secretKey'         : Rule(type=str, required=False),
    'installationSiteId': Rule(type=int, required=True)
}


@bp.route('/add', methods=['post'])
@pre.catch(add_device_rules)
def add_device(params):
    session = session_maker()
    inst_site_id = params['installationSiteId']
    if inst_site_id == 0:
        inst_site_id = None
    inst_site = session.execute(
        select(DeviceInstallationSite).where(DeviceInstallationSite.id == inst_site_id)
    ).scalar()
    if inst_site is None:
        return resp(400, '不存在的安装场所')
    d = Device()
    d.name = params['deviceName']
    d.description = params['description']
    d.secret_key = params['secretKey']
    d.installation_site_id = inst_site_id
    d.uuid = uuid.uuid1()
    session.add(d)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return resp()


device_status_rules = {
    'ids': Rule(type=list, required=True)
}


@bp.route('/get_status', methods=['post'])
@pre.catch(device_status_rules)
def device_status(params):
    ids: List[int] = params['ids']
    # rets = grpc_stub.GetDeviceStatus.future(ids.__iter__())
    ret = {}
    for r in grpc_stub.GetDeviceStatus([device_pb2.DeviceId(id=id) for id in ids].__iter__()):
        ret[int(r.id)] = r.status
    return resp(rst=ret)


get_rules = {
    'id': Rule(type=int, required=True)
}


@bp.route('/get', methods=['post'])
@pre.catch(get_rules)
def get(params):
    id = params['id']
    session = session_maker()
    ret = session.execute(
        select(Device).where(Device.id == id)
    ).scalar()
    session.close()
    return resp(rst=ret)


@bp.route('/get_all_status', methods=['post'])
def get_all_status():
    session = session_maker()
    ids = session.execute(
        select(distinct(Device.id))
    ).scalars().all()
    ret_malfunc = []
    ret_stopped = []
    ret_running = []
    for id in ids:
        r = session.execute(
            select(DeviceEvent, DeviceEventStatusChange).where(
                and_(
                    or_(
                        DeviceEventStatusChange.status == constant.DeviceStatus.MALFUNC,
                        DeviceEventStatusChange.status == constant.DeviceStatus.STOPPED,
                        DeviceEventStatusChange.status == constant.DeviceStatus.RUNNING,
                    ),
                    DeviceEvent.device_id == id
                )
            ).order_by(desc(DeviceEvent.created_at)).limit(1)
        ).scalar()
        if r is None:
            continue
        if r.status == constant.DeviceStatus.MALFUNC:
            ret_malfunc.append(r)
        elif r.status == constant.DeviceStatus.STOPPED:
            ret_stopped.append(r)
        else:
            ret_running.append(r)
    session.close()
    return resp(rst={'malfunc': ret_malfunc, 'stopped': ret_stopped, 'running': ret_running})
