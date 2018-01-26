# -*- coding: utf-8 -*-
from functools import wraps
from json import JSONDecoder, JSONEncoder
from enum.enum import IntEnum
from flask import request
from sqlalchemy import or_
from Models.CloudStorge import User, Domain, ShareUserCache, Object, StorageShare
from Models.Database import db
from Tools.APIException import APIException, AuthErrorCode, DataErrorCode, SystemErrorCode, HandleStatusErrorCode
from Tools.SqliteSession import ManualSession
from Models.Platform import ContractAttachment, ContractUserGroup, ContractAttachmentType, RequirementAttachment, \
    ResourceShare
from sqlalchemy.orm.exc import NoResultFound

def GetSessionId():
    request.sessionId = None
    try:
        try:
            data = request.json_param
        except:
            data = JSONDecoder().decode(request.data)
        request.sessionId = data[u'DBToken']
    except:
        try:
            request.sessionId = request.values[u'DBToken']
        except:
            try:
                request.sessionId = request.cookies[u'DBToken']
            except:
                pass
    return request.sessionId


def PermissionValidate(Permission=None):
    def wrapper_func_permission(resource):
        @wraps(resource)
        def wrapper(*args, **kwargs):
            SessionId = GetSessionId()
            exception = JSONEncoder(ensure_ascii=False).encode(
                APIException(SystemErrorCode.SessionIdInvalid, u'DBToken无效', request.path))
            if SessionId is None:
                return exception
            request.session = None
            try:
                request.session = ManualSession().open_session(sid=SessionId)
            except:
                pass
            if request.session is None:
                return exception
            if Permission is not None:
                pass  #TODO:权限认证
            return resource(*args, **kwargs)

        return wrapper

    return wrapper_func_permission


def refresh_user_permission(session, user):
    session["domainPermissionWrite"] = session["domainPermissionCreate"] = session["domainPermissionShare"] = session[
        "domainPermissionDelete"]=session["domainPermissionDownload"]= 0
    for role in user.Roles:
        if session["domainPermissionWrite"] == 0 and role.DomainWrite == 1:
            session["domainPermissionWrite"] = 1
        if session["domainPermissionCreate"] == 0 and role.DomainCreate == 1:
            session["domainPermissionCreate"] = 1
        if session["domainPermissionShare"] == 0 and role.DomainShare == 1:
            session["domainPermissionShare"] = 1
        if session["domainPermissionDelete"] == 0 and role.DomainDelete == 1:
            session["domainPermissionDelete"] = 1
        if session["domainPermissionDownload"] == 0 and role.DomainDownload == 1:
            session["domainPermissionDownload"] = 1


class Permission(IntEnum):
    PermissionRead, PermissionWrite, PermissionCreate, PermissionShare, PermissionDelete, PermissionDownload = range(0, 6)


# 测试某个object对象是否有被当前用户访问的权限
def sharedPermissionValidate(PermissionRequired=Permission.PermissionRead, prefix=u'', param=None):
    if param is None:
        param = request.json_param

    permissions = None
    domainid = prefix + u'DomainId'
    shareid = prefix + u'ShareId'
    rootObject = None
    # 带有domainId，object属于某域用户
    if domainid in param:
        domainId = request.session["DomainId"]
        # 如果当前用户和object所属owner所在域相同，则获取object的userid
        if int(param[domainid]) == domainId:
            UserId = db.session.query(Domain.OwnerUserId).filter_by(Id=domainId).one()[0]
        else:
            raise APIException(SystemErrorCode.UnkonwnError, u'无权限执行操作')
    # 带有shardeId，说明object是某个共享对象
    elif shareid in param:
        ShareId = param[shareid]
        shareusercacheall = ShareUserCache.query.filter(or_(ShareUserCache.UserId == request.session['UserId'],
                                                            ShareUserCache.UserId == 0),#判断是否同事共享给所有用户
                                                     ShareUserCache.ShareObjectId == ShareId).all()
        for permission in permissions:
            try:
                shareusercache = shareusercacheall[0]
                raise APIException(SystemErrorCode.UnkonwnError, u'无权限执行操作')
            except IndexError:
                if len(shareusercacheall) == 2: #如果共享给所有用户 计算合并后权限
                    shareusercache = shareusercacheall[0]
                for i in range(1,len(shareusercacheall)):
                    for permission in permissions:
                        if shareusercache.__dict__['User' + permission.name[10:]]!=1:
                            shareusercache.__dict__['User' + permission.name[10:]]=shareusercacheall[i].__dict__['User' + permission.name[10:]]
            if permission == Permission.PermissionShare or shareusercache.__dict__['User' + permission.name[10:]] != 1:
                raise APIException(SystemErrorCode.UnkonwnError, u'无权限执行操作')
        UserId = shareusercache.ShareObject.CreatorUserId
        rootObject = shareusercache.ShareObject.Object
    else:
        UserId = request.session["UserId"]
    if rootObject is None:
        rootObject = Object.query.filter_by(ParentId=None, OwnerUserId=UserId).one()
    if int(param[prefix + u'Id']) != 0 and Object.query.filter(Object.Id == param[prefix + u'Id'], Object._Left_ >= rootObject._Left_,
                           Object._Right_ <= rootObject._Right_, Object.OwnerUserId == UserId).count() == 0:
        raise APIException(SystemErrorCode.UnkonwnError, u'无权限执行操作')
    return UserId


def objectOperatePermission(object_id, user_id, context, operation):
    bWrite = True
    bDownload = True
    bRead = True
    try:
        obj = Object.query.filter_by(Id=object_id).one()
    except NoResultFound:
        raise APIException(DataErrorCode.NoRecord, '无该访问资源')
    if context == 'contractAttachment':
        ca = ContractAttachment.query.filter_by(ObjectId=object_id).all()
        if len(ca) == 0:
            raise APIException(DataErrorCode.NoRecord, '无该访问合同附件')
        for a in ca:
            if a.Type == ContractAttachmentType.Exchange \
                    or a.Type == ContractAttachmentType.Clip \
                    or a.Type == ContractAttachmentType.CutVideo \
                    or a.Type == ContractAttachmentType.RenderVideo \
                    or a.Type == ContractAttachmentType.SoundVideo \
                    or a.Type == ContractAttachmentType.FinalVideo:
                bDownload = True
                bWrite = True
            elif a.Type == ContractAttachmentType.End:
                bDownload = True
                bWrite = False
        try:
            ContractUserGroup.query.filter_by(ContractId=ca[0].ContractId, UserId=user_id).one()
        except NoResultFound:
            raise APIException(DataErrorCode.NoRecord, '无该合同用户')
    elif context == 'requirementAttachment':
        user = User.query.filter_by(Id=user_id).one()
        ra = RequirementAttachment.query.filter_by(ObjectId=object_id).all()
        if len(ra) == 0:
            raise APIException(DataErrorCode.NoRecord, '无该需求附件')
        rs = ResourceShare.query.filter_by(ResourceId=ra[0].RequirementId, ResourceType='r').all()
        for r in rs:
            if r.ShareDomainId == 0 or r.ShareDomainId == user.DomainId:
                bWrite = True
                bDownload = True
                break
    elif context == 'storage':
        owner = User.query.filter_by(Id=obj.OwnerUserId).one()
        user = User.query.filter_by(Id=user_id).one()
        if owner.DomainId != user.DomainId:
            try:
                StorageShare.query.filter_by(ObjectId=obj.Id, DomainId=user.DomainId).one()
            except NoResultFound:
                raise APIException(SystemErrorCode.NonPermissionHandle, '无权限访问该资源')
    if operation == 'download':
        if not bDownload:
            raise APIException(SystemErrorCode.NonPermissionHandle, '无权限访问该资源')
    elif operation == 'delete' or operation == 'move' or operation == 'write':
        if not bWrite:
            raise APIException(SystemErrorCode.NonPermissionHandle, '无权限访问该资源')
    elif operation == 'read':
        if not bRead:
            raise APIException(SystemErrorCode.NonPermissionHandle, '无权限访问该资源')
    return obj.OwnerUserId