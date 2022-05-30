import json

import redis as redis
from flask import Flask
from flask_cors import CORS
from pre_request import pre
from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import HTTPException

from client_grpc import init_grpc
from config import AppConfig
from util.response import CustomResponse, resp

app = Flask(__name__, static_url_path='/', static_folder='web')
# 读取配置
app.config.from_object(AppConfig)
app.config.from_file('config.json', json.load)
# mysql数据库连接
db_engine = create_engine(
    f'mysql://{app.config.get("MYSQL_USER")}:{app.config.get("MYSQL_PASS")}'
    f'@{app.config.get("MYSQL_HOST")}:{app.config.get("MYSQL_PORT")}/{app.config.get("MYSQL_DB")}',
    pool_size=5,
    max_overflow=0,
    pool_pre_ping=True,
    # echo=True
)
session_maker = sessionmaker(db_engine)
# redis连接
redis_client = redis.Redis(
    host=app.config.get('REDIS_HOST'),
    port=app.config.get('REDIS_PORT'),
    db=app.config.get('REDIS_DB'),
)

# init grpc
grpc_channel, grpc_stub = init_grpc()


def init_app():
    # 装载数据库模型
    # import database.mysql.model
    from database.mysql.model.base import Base
    Base.metadata.create_all()
    # 装载蓝图
    from api.installation_site import bp as LocationBp
    from api.device import bp as DeviceBp
    from api.device_config import bp as DeviceConfigBp
    from api.device_info import bp as DeviceInfoBp
    from api.device_event import bp as DeviceEventBp
    from api.device_version import bp as DeviceVersionBp
    from api.device_log import bp as DeviceLogBp
    from api.device_data import bp as DeviceDataBp
    app.register_blueprint(LocationBp)
    app.register_blueprint(DeviceBp)
    app.register_blueprint(DeviceConfigBp)
    app.register_blueprint(DeviceInfoBp)
    app.register_blueprint(DeviceEventBp)
    app.register_blueprint(DeviceVersionBp)
    app.register_blueprint(DeviceLogBp)
    app.register_blueprint(DeviceDataBp)
    # 装载参数校验工具
    pre.init_app(app)
    # pre.add_response(CustomResponse)
    # 跨域
    CORS(app)

    # 错误处理
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps(resp(e.code, e.name))
        response.content_type = 'application/json'
        return response

    return app


if __name__ == '__main__':
    init_app()
    app.run(port=9090, debug=True)
