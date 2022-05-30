from .common import *

bp = Blueprint('installation_site', __name__, url_prefix='/installation_site')

list_location_rules = {
    'parent': Rule(type=int, required=False, default=None)
}


@bp.route('/get_tree', methods=['post'])
@pre.catch(list_location_rules)
def get_tree(params):
    session = session_maker()
    locs = session.execute(
        select(DeviceInstallationSite)
            .where(DeviceInstallationSite.pid == params['parent'])
            # .options(immediateload(DeviceInstallationSite.sub_installation_sites))
    ).scalars().all()
    session.close()
    return resp(rst=locs)


set_location_parent_rules = {
    'self'  : Rule(type=int, required=True),
    'parent': Rule(type=int, required=True)
}


@bp.route('/set_parent', methods=['post'])
@pre.catch(set_location_parent_rules)
def set_parent(params):
    session = session_maker()
    self_id = params['self']
    new_parent_id = params['parent']
    if new_parent_id == 0:
        new_parent_id = None  # None 真正代表根节点（当然根节点记录并不存在）
    # 目标节点的路径树上，不包含self即可
    operand_inst_site: DeviceInstallationSite = session.execute(
        select(DeviceInstallationSite).where(DeviceInstallationSite.id == self_id)
    ).scalar()
    new_parent_inst_site: Optional[DeviceInstallationSite] = session.execute(
        select(DeviceInstallationSite).where(DeviceInstallationSite.id == new_parent_id)
    ).scalar()
    if (new_parent_id is not None and new_parent_inst_site is None) or operand_inst_site is None:
        return resp(404, '不存在的安装场所')
    if operand_inst_site.pid == new_parent_id:
        return resp(400, '无效操作')
    while new_parent_inst_site is not None:
        if new_parent_inst_site.id == self_id:
            return resp(400, '无效操作')
        new_parent_inst_site: DeviceInstallationSite = session.execute(
            select(DeviceInstallationSite).where(DeviceInstallationSite.id == new_parent_inst_site.pid)
        ).scalar()
    session.add(operand_inst_site)
    operand_inst_site.pid = new_parent_id
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return resp()


add_location_rules = {
    'parent'     : Rule(type=int, required=False, default=0),
    'name'       : Rule(type=str, required=True, gte=1, lte=100),
    'description': Rule(type=str, required=False)
}


@bp.route('/add', methods=['post'])
@pre.catch(add_location_rules)
def add(params):
    session = session_maker()
    parent_id = params['parent']
    if parent_id == 0:
        parent_id = None
    parent: DeviceInstallationSite = session.execute(
        select(DeviceInstallationSite).where(DeviceInstallationSite.id == parent_id)
    ).scalar()
    if parent_id is not None and parent is None:
        return resp(400, '不存在的父节点')
    new_inst_site = DeviceInstallationSite()
    new_inst_site.pid = parent_id
    new_inst_site.name = params['name']
    new_inst_site.description = params['description']
    session.add(new_inst_site)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return resp()


delete_location_rules = {
    'id': Rule(type=int, required=True)
}


@bp.route('/delete', methods=['post'])
@pre.catch(delete_location_rules)
def delete(params):
    session = session_maker()
    id = params['id']
    # 检查是否存在
    inst_site_to_delete: DeviceInstallationSite = session.execute(
        select(DeviceInstallationSite).where(DeviceInstallationSite.id == id)
    ).scalar()
    if inst_site_to_delete is None:
        return resp(400, '不存在的安装场所')
    # 检查有无下级场所
    sub_inst_sites = session.execute(
        select(DeviceInstallationSite).where(DeviceInstallationSite.pid == id)
    ).scalars().all()
    if len(sub_inst_sites) > 0:
        return resp(400, '该场所存在下级场所，不能直接删除')
    # 检查是否有关联设备
    devices = session.execute(
        select(Device).where(Device.installation_site_id == id)
    ).scalars().all()
    if len(devices) > 0:
        return resp(400, '该场所存在相关联的设备/边缘计算客户端')
    # 删除它
    session.delete(inst_site_to_delete)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return resp()


edit_location_rules = {
    'id'         : Rule(type=int, required=True),
    'name'       : add_location_rules['name'],
    'description': add_location_rules['description']
}


@bp.route('/edit', methods=['post'])
@pre.catch(edit_location_rules)
def edit(params):
    session = session_maker()
    editable_location: DeviceInstallationSite = session.execute(
        select(DeviceInstallationSite).where(DeviceInstallationSite.id == params['id'])
    ).scalar()
    if editable_location is None:
        return resp(400, '不存在的安装场所')
    editable_location.name = params['name']
    editable_location.description = params['description']
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return resp()
