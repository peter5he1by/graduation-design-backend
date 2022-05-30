from .common import *

bp = Blueprint('device_version', __name__, url_prefix='/device/version')

add_rules = {
    'codeName'       : Rule(type=str, required=False),
    'internalVersion': Rule(type=int, required=True),
    'externalVersion': Rule(type=str, required=False),
    'fileUrl'        : Rule(type=str, required=True),
    'hashValue'      : Rule(type=str, required=True),
}


@bp.route('/add', methods=['post'])
@pre.catch(add_rules)
def add(params):
    code_name = params.get('codeName')
    internal_version = params.get('internalVersion')
    external_version = params.get('externalVersion')
    file_url = params.get('fileUrl')
    hash_value = params.get('hashValue')
    v = DeviceVersion()
    v.code_name = code_name
    v.internal_version = internal_version
    v.external_version = external_version
    v.file_url = file_url
    v.hash_value = hash_value
    session = session_maker()
    session.add(v)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return resp()


@bp.route('/get_list', methods=['post'])
def get_list():
    session = session_maker()
    ret = session.execute(
        select(DeviceVersion).order_by(desc(DeviceVersion.updated_at))
    ).scalars().all()
    session.close()
    return resp(rst=ret)


edit_rules = {
    'id'             : Rule(type=int, required=True),
    'codeName'       : Rule(type=str, required=False),
    'internalVersion': Rule(type=int, required=True),
    'externalVersion': Rule(type=str, required=False),
    'fileUrl'        : Rule(type=str, required=True),
    'hashValue'      : Rule(type=str, required=True),
}


@bp.route('/edit', methods=['post'])
@pre.catch(edit_rules)
def edit(params):
    id = params.get('id')
    code_name = params.get('codeName')
    internal_version = params.get('internalVersion')
    external_version = params.get('externalVersion')
    file_url = params.get('fileUrl')
    hash_value = params.get('hashValue')
    session = session_maker()
    v = session.query(DeviceVersion).get(id)
    if v is None:
        return resp(404, '该版本信息不存在')
    v.code_name = code_name
    v.internal_version = internal_version
    v.external_version = external_version
    v.file_url = file_url
    v.hash_value = hash_value
    session.add(v)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return resp()
