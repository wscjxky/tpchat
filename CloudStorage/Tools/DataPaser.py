#-*- coding: utf-8 -*-
from functools import wraps
from datetime import datetime
from json import JSONDecoder
from flask import Response, request
from flask.ext.restful import unpack
from sqlalchemy.orm import Query
from sqlalchemy.orm.dynamic import AppenderMixin
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from Tools.APIException import APIException, get_error_log_str,SystemErrorCode
from Tools.TimezoneTool import get_mysqltz
from sqlalchemy.orm.state import InstanceState
from dateutil import tz

def expandAttribute(obj, expand_list):
    def expand(obj,expand_list=expand_list):
        dict = obj.__dict__
        for ea in expand_list:
            eaChilren = None
            try:
                index = ea.index(':')
                eaChilren = eval(ea[index+1:])
                ea = ea[:index]
            except ValueError:
                pass
            av = eval('obj.' + ea)
            if isinstance(av, Query) or isinstance(av, AppenderMixin):
                dict[ea] = av.all()
            else:
                dict[ea] = av
            if eaChilren is not None:
                expandAttribute(dict[ea], eaChilren)
        return dict

    if isinstance(obj, list):
        r = [expand(o) for o in obj]
    else:
        r = expand(obj)
    return r

def convert_to_builtin_type(self, obj):
    if isinstance(obj, InstanceState):
        return None
    if isinstance(obj, datetime):
        if obj.tzinfo is None:
            return obj.replace(tzinfo=get_mysqltz()).astimezone(tz.tzutc()).isoformat()
        else:
            return obj.astimezone(tz.tzutc()).isoformat()
    d = {}
    d.update(obj.__dict__)
    remove_attribute = ['__class__', '__module__', '_sa_instance_state']
    remove_attribute.extend(Convertor.convert_to_builtin_type_remove_attribute)
    for item in remove_attribute:
        try:
            d.__delitem__(item)
        except Exception:
            pass

    if 'Image' in d and d['Image'] is not None:  # TODO: 转换绝对路径修改 因为可能会出问题，比如非Image字段的静态资源
        d['Image'] = request.host_url + d['Image']
    return d


class Convertor:
    #TODO:多并发条件下不知道是否可以正常运行
    convert_to_builtin_type_remove_attribute = []


def method_post_only(resource):
    @wraps(resource)
    def wrapper(*args, **kwargs):
        if request.method == 'GET':
            return APIException(40400, u'API提交方式错误', request.path)
        return resource(*args, **kwargs)

    return wrapper


def output_data_without_attribute(RemoveAttribute):
    RemoveAttribute.extend(['Password', 'SessionId', 'MD5'])
    def warpper_func(resource):
        @wraps(resource)
        def wrapper(*args, **kwargs):
            Convertor.convert_to_builtin_type_remove_attribute.__init__()
            Convertor.convert_to_builtin_type_remove_attribute.extend(RemoveAttribute)
            resp = resource(*args, **kwargs)
            return resp

        return wrapper

    return warpper_func


jsonDecoder = JSONDecoder()
def get_json_param():
    if request.json is not None:
        return request.json
    isDataJson = False
    try:
        isDataJson = str(request.content_type).upper().index('JSON')
    except ValueError:
        pass
    if isDataJson:
        return jsonDecoder.decode(request.data)
    else:
        try:
            return jsonDecoder.decode(request.data)
        except Exception:
            try:
                return jsonDecoder.decode(request.values['json'])
            except:
                try:
                    return JSONDecoder.decode(request.form['json'])
                except:
                    try:
                        result={}
                        def addToResult(result,list):
                            if len(request.values)>0:
                                for k in request.values:
                                    if k not in result:
                                        result[unicode(k)] = unicode(request.values[k])
                        addToResult(result,request.values)
                        addToResult(result,request.form)
                        return result
                    except:
                        return None


def output_data(resource):
    @wraps(resource)
    def wrapper(*args, **kwargs):
        request.json_param = get_json_param()
        e = None
        try:
            resp = resource(*args, **kwargs)
        except APIException as e:
            resp = e
        except KeyError as e:
            resp = APIException(SystemErrorCode.ArgumentError, u'参数错误', request.path)
        except ValueError as e:
            resp = APIException(SystemErrorCode.ArgumentError, u'参数错误', request.path)
        except MultipleResultsFound as e:
            resp = APIException(SystemErrorCode.DataError, u'数据不唯一', request.path)
        except NoResultFound as e:
            resp = APIException(SystemErrorCode.DataError, u'数据不存在', request.path)
        except Exception as e:
            resp = APIException(SystemErrorCode.UnkonwnError, u'未知错误', request.path)

        if isinstance(resp, Response):  # There may be a better way to test
            return resp
        if isinstance(resp, APIException):
            print((resp.to_str()))
            if (e is not None):
                print get_error_log_str()
        data, code, headers = unpack(resp)
        from Main import api
        resp = api.make_response(data, code, headers=headers)
        if 'jsonpCallback' in request.values:
            jsonpCallback = request.values['jsonpCallback']
            resp.data = str(jsonpCallback)+'('+resp.data+');'
        try:
            request.session.close()  # 关闭Session
        except AttributeError:
            pass
        return resp

    return wrapper


def incoming_params(resource):
    @wraps(resource)
    def wrapper(*args, **kwargs):
        request.json_param = get_json_param()
        e = None
        try:
            resp = resource(*args, **kwargs)
        except APIException as e:
            resp = e
        except KeyError as e:
            resp = APIException(SystemErrorCode.ArgumentError, u'参数错误', request.path)
        except ValueError as e:
            resp = APIException(SystemErrorCode.ArgumentError, u'参数错误', request.path)
        except MultipleResultsFound as e:
            resp = APIException(SystemErrorCode.DataError, u'数据不唯一', request.path)
        except NoResultFound as e:
            resp = APIException(SystemErrorCode.DataError, u'数据不存在', request.path)
        except Exception as e:
            resp = APIException(SystemErrorCode.UnkonwnError, u'未知错误', request.path)

        if isinstance(resp, Response):  # There may be a better way to test
            return resp
        if isinstance(resp, APIException):
            print((resp.to_str()))
            if (e is not None):
                print get_error_log_str()
        if 'jsonpCallback' in request.values:
            jsonpCallback = request.values['jsonpCallback']
            resp.data = str(jsonpCallback)+'('+resp.data+');'
        return resp

    return wrapper


def round_(amount, decimal=2):
    return round(amount, decimal)