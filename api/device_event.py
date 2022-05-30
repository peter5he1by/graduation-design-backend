from .common import *

bp = Blueprint('device-event', __name__, url_prefix='/device/event')

get_rules = {
    'id': Rule(type=int, required=True)
}


@bp.route('/get', methods=['post'])
@pre.catch(get_rules)
def get(params):
    id = params['id']
    session = session_maker()
    # device = session.execute(
    #     select(DeviceEvent).where(DeviceEvent.device_id == id).order_by(desc(DeviceEvent.created_at))
    # ).scalars().all()
    # session.close()
    device = session.query(Device).filter(Device.id == id).options(
        subqueryload(
            Device.events.of_type(DeviceEventStatusChange)
        ),
        subqueryload(
            Device.events.of_type(DeviceEventLogin)
        ),
        subqueryload(
            Device.events.of_type(DeviceEventLogout)
        ),
        subqueryload(
            Device.events.of_type(DeviceEventOperation)
        ),
    ).one()
    events: list = device.events
    events.sort(key=lambda event: event.created_at.timestamp(), reverse=True)
    session.close()
    return resp(rst=events)
