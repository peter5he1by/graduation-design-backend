import pytz

import constant
from .common import *

bp = Blueprint('device-data', __name__, url_prefix='/device/data')

get_temperature_rules = {
    'id'       : Rule(type=int, required=True),
    'timeAfter': Rule(type=datetime, required=True, fmt="%Y-%m-%dT%H:%M:%S%z")
}


@bp.route('/get_temperature', methods=['POST'])
@pre.catch(get_temperature_rules)
def get_temperature(params):
    id = params.get('id')
    # 先看设备状态
    ret = {}
    for r in grpc_stub.GetDeviceStatus([device_pb2.DeviceId(id=id) for id in [id]].__iter__()):
        ret[r.id] = r.status
    if ret[id] == constant.DeviceStatus.STOPPED:
        return resp(500, '设备停止')
    time_after: datetime = params.get('timeAfter')
    time_after = time_after.astimezone(pytz.UTC)  # 数据库存的是UTC时间，比较的时候得按UTC格式比较
    sess = session_maker()
    ret = sess.execute(
        select(DeviceDataTemperature)
            .where(
            DeviceDataTemperature.time > time_after,
            DeviceDataTemperature.device_id == id
        )
    ).scalars().all()
    sess.close()
    return resp(rst=ret)
