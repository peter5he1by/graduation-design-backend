import json
from typing import Callable, Optional

from pre_request import BaseResponse, ParamsValueError


def resp(code: int = 200, msg: str = '', rst=None):
    return {'respCode': code, 'respMsg': msg, 'result': rst}


class CustomResponse(BaseResponse):

    def make_response(
            self,
            error: "ParamsValueError",
            fuzzy: bool = False,
            formatter: Optional[Callable] = None
    ):
        print(error)
        print(fuzzy)
        result = {
            "respCode": 400,
            "respMsg" : error,
            "result"  : {}
        }
        from flask import make_response  # pylint: disable=import-outside-toplevel
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
