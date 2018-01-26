# -*- coding: utf-8 -*-
from json.encoder import JSONEncoder

from flask import request
import StringIO
from datetime import datetime
import traceback
import sys
from enum import IntEnum


class ErrorCodeEnum(IntEnum):
    def __str__(self):
        return str(self.value)


#系统错误码
class SystemErrorCode(ErrorCodeEnum):
    NotAllowAmend = 0  #不允许修改
    OnlySupportHttps = 1  #仅支持https请求
    NonSupportFileType = 2  #不支持的文件类型
    SessionIdInvalid = 3  #SessionId无效
    SessionIdCannotNone = 4  #SessioniId不能是空
    UnkonwnError = 5  #
    NonPermissionCreate = 6  #没有权限创建
    NonPermissionDelete = 7  #没有权限删除
    NonPermissionUpload = 8  #没有权限上传
    ArgumentError = 9
    DataError = 10
    CrashError = 11
    NonPermissionAllot = 12  #没有权限分配
    NonPermissionHandle = 13  #没有权限执行此操作


#授权错误码
class AuthErrorCode(ErrorCodeEnum):
   # __last_number__ = 1000
    UserStillOnline = 1000  #用户仍在线
    LoginTimeout = 1001  #登陆超时
    UserNotLogined = 1002  #用户没有登陆
    UserNotActived = 1003  #需要激活码
    UserOrPassIncorrect = 1004  #用户名或密码错误
    UserNameCreated = 1005  #用户名已被占用
    UserAlreadyActive = 1006  #用户已经激活
    ProductAuthFail = 1007  #产品授权失败
    MachineCodeRequired = 1008  #必须提供机器码


#数据错误码
class DataErrorCode(ErrorCodeEnum):
    RoleNameInexistence = 2000  #角色名不存在
    InvalidFriendUserId = 2001  #无效的用户名
    ActiveCodeIncorrect = 2002  #激活码错误
    VersionInexistence = 2003  #版本不存在
    NoRecord = 2004  #没有记录
    FileAlreadyExist = 2005 #文件已存在
    NoStorageSize = 2006  #  存储空间不足
    DomainNameExist = 2007  #域名已存在
    UserInexistence = 2008  #用户不存在
    DomainRoleExist = 2009  #域角色已存在
    StatusError = 3004  #状态错误


#操作状态错误码
class HandleStatusErrorCode(ErrorCodeEnum):
    RechargeFail = 3000  #充值失败
    CreateFailed = 3001  #创建失败，目录已存在
    UploadSuccess = 3002  #上传成功
    UploadFaild = 3003  #上传失败



def GetErrorCodeDefinations():
    ErrorCodeClasses = [DataErrorCode, AuthErrorCode, SystemErrorCode,
                        HandleStatusErrorCode]  #TODO:定义的错误码类加入这个列表，用于生成C++对应enum类型
    import cStringIO
    import os

    strio = cStringIO.StringIO()
    for ErrorCodeClass in ErrorCodeClasses:
        ErrorCodesCount = len(ErrorCodeClass)
        strio.write('typedef enum _' + ErrorCodeClass.__name__ + '{')
        strio.write(os.linesep)
        for i in range(0, ErrorCodesCount):
            ErrorCode = ErrorCodeClass[list(ErrorCodeClass.__members__)[i]]
            strio.write('\t' + ErrorCode.name + '=' + str(ErrorCode.value))
            if i != ErrorCodesCount - 1:  #最后一个不打印,
                strio.write(',')
            strio.write(os.linesep)
        strio.write('}' + ErrorCodeClass.__name__ + ';')
    print strio.getvalue()


class StringIO:
    str = u""

    def __init__(self):
        pass

    def write(self, str):
        try:
            self.str += str
        except UnicodeDecodeError as e:
            self.str += unicode(str, 'utf-8')

    def getvalue(self):
        return self.str


from flask import request
from datetime import datetime
import traceback
import sys


def get_error_log_str():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    strio = StringIO()
    strio.write(u"================ Begin =================\r\n")
    strio.write(u"Time:" + datetime.now().isoformat() + "\r\n")
    strio.write(u"api:" + request.full_path + "\r\n")
    strio.write(u"method:" + request.method + "\r\n")
    strio.write(u"content_tpye:" + request.content_type + "\r\n")
    strio.write(u"data:" + request.data.decode('utf-8') + "\r\n")
    strio.write(u"Stack Trace:\r\n")
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=strio)
    strio.write(u"================  End  =================\r\n")
    result = strio.getvalue()
    return result


def all_exception_handler(e):
    print get_error_log_str()
    if isinstance(e,APIException):
        return JSONEncoder(ensure_ascii=False).encode(e)
    return JSONEncoder(ensure_ascii=False).encode(
        APIException(SystemErrorCode.CrashError, u"遇到严重错误！问题已经记录，稍后管理员将进行修复，请稍后再试！", request.path))


class APIException(Exception):
    errorCode = 0
    errorMsg = ''
    apiName = ''

    def __init__(self, error_code, error_msg, apiName=None):
        self.errorCode = error_code
        self.errorMsg = error_msg
        if apiName is None:
            self.apiName = request.path
        else:
            self.apiName = apiName

    def to_str(self):
        return JSONEncoder(ensure_ascii=False).encode(
            {u"errorCode": self.errorCode, u"errorMsg": self.errorMsg, u"apiName": self.apiName})

