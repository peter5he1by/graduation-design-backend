from .common import *

bp = Blueprint('device-info', __name__, url_prefix='/device/info')

get_rules = {
    'id': Rule(type=int, required=True),
    # 'pageNum' : Rule(type=int, required=False, default=1, gt=0),
    # 'pageSize': Rule(type=int, required=False, default=20),
}


@bp.route('/get', methods=['post'])
@pre.catch(get_rules)
def get(params):
    id = params['id']
    # page_num = params['pageNum']
    # page_size = params['pageSize']
    session = session_maker()
    # total = session.scalar(
    #     select(func.count())
    #         .select_from(DeviceInfo)
    #         .where(DeviceInfo.device_id == id)
    # )
    infos = session.execute(
        select(DeviceInfo)
            .where(DeviceInfo.device_id == id)
            .order_by(desc(DeviceInfo.updated_at))
            .limit(1000)
        # .offset((page_num - 1) * page_size)
    ).scalars().all()
    session.close()
    return resp(rst={
        # 'pageNum' : page_num,
        # 'pageSize': page_size,
        # 'total'   : total,
        'infos': infos
    })
