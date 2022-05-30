import io
import json
from xml.etree import ElementTree

import yaml

from .common import *

bp = Blueprint('device-config', __name__, url_prefix='/device/config')

get_rules = {
    'id': Rule(type=int, required=True)
}


@bp.route('/get_new', methods=['post'])
@pre.catch(get_rules)
def get(params):
    id = params['id']
    try:
        d: device_pb2.DeviceConfig = grpc_stub.GetDeviceConfig(device_pb2.DeviceId(id=id))
    except:
        print('grpc returned error')
        return resp()
    session = session_maker()
    if d.id == 0:
        d: DeviceConfig = session.execute(
            select(DeviceConfig).where(DeviceConfig.device_id == id).order_by(desc(DeviceConfig.updated_at))
        ).scalar()
        session.close()
        return resp(msg='设备不在线或未响应|获取最近一次配置', rst=d)
    d: DeviceConfig = session.execute(
        select(DeviceConfig).where(DeviceConfig.id == d.id)
    ).scalar()
    session.close()
    return resp(rst=d)


set_rules = {
    'id'     : Rule(type=int, required=True),
    'content': Rule(type=str, required=True)
}


@bp.route('/set', methods=['post'])
@pre.catch(set_rules)
def set(params):
    id = params['id']
    content: str = params['content']
    session = session_maker()
    d: DeviceConfig = session.execute(
        select(DeviceConfig).order_by(desc(DeviceConfig.updated_at))
    ).scalar()
    config_type = d.type
    if config_type == 'json':
        try:
            json.loads(content)
        except:
            return resp(400, 'json格式不正确|设备配置格式为json')
    elif config_type == 'xml':
        try:
            ElementTree.parse(io.BytesIO(content.encode()))
        except Exception as e:
            print(e)
            return resp(400, 'xml格式不正确|设备配置格式为xml')
    elif config_type == 'yaml':
        try:
            yaml.load(content)
        except:
            return resp(400, 'yaml格式不正确|设备配置格式为yaml')
    else:
        return resp(400, '平台不支持的配置文件格式')
    try:
        res = grpc_stub.SetDeviceConfig(device_pb2.DeviceConfig(id=id, content=content))
    except:
        return resp(500, "error")
    if res.ret == 0:
        return resp()
    if res.ret == 1:
        return resp(500, "设备不在线")
    return resp(500, "下发失败")
