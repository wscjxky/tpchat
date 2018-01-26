#-*- coding: utf-8 -*-
from functools import wraps
from json import JSONEncoder
from flask import current_app, request
from Tools.APIException import APIException, AuthErrorCode,DataErrorCode,SystemErrorCode,HandleStatusErrorCode


def ssl_only(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return JSONEncoder(ensure_ascii=False).encode(APIException(SystemErrorCode.OnlySupportHttps, u"仅支持Https方式访问该接口"))
        return fn(*args, **kwargs)
    return decorated_view