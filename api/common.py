import logging
from datetime import datetime, timedelta
import uuid
from typing import List, Optional

from flask import Blueprint
from pre_request import Rule, pre
from sqlalchemy.future import select
from sqlalchemy.orm import immediateload, joinedload, noload, subqueryload
from sqlalchemy import desc, text, or_, and_, distinct
from sqlalchemy.sql.expression import func

import constant
from client_grpc.device import device_pb2
from database.mysql.model import Device, DeviceInstallationSite
from database.redis import key
from main import db_engine, redis_client, session_maker, grpc_stub
from util.response import resp

from database.mysql.model import *
