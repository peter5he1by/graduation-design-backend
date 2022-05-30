import io

from flask import send_file

from .common import *

bp = Blueprint('device-log', __name__, url_prefix='/device/log')

get_list_rules = {
    'id': Rule(type=int, required=True),
}


@bp.route('/get_list', methods=['post'])
@pre.catch(get_list_rules)
def get_list(params):
    id = params.get('id')
    session = session_maker()
    ret = session.execute(
        select(DeviceLog).order_by(desc(DeviceLog.start_time))
    ).scalars().all()
    # ret = session.query(DeviceLog).filter_by(device_id=id).order_by('device_id').all()
    session.close()
    return resp(rst=ret)


@bp.route('/get_content', methods=['post'])
@pre.catch(get_list_rules)
def get_content(params):
    id = params.get('id')
    session = session_maker()
    log = session.query(DeviceLog).get(id)
    content = log.content
    if len(content) > 4609:
        content = content[-4608:]
    session.close()
    return resp(rst={'content': content, 'size': len(log.content)})


@bp.route('/download', methods=['get'])
@pre.catch(get_list_rules)
def download(params):
    id = params['id']
    session = session_maker()
    log = session.query(DeviceLog).get(id)
    content: str = log.content
    reader = io.BytesIO(content.encode())
    session.close()
    return send_file(reader, as_attachment=True, download_name='device.log', mimetype='text/plain')
