# -*- coding: utf-8 -*-
from enum import IntEnum
from sqlalchemy.sql import functions
from Models.CloudStorge import Domain, DomainStatus, Share, ShareUserCache, ShareUser, ObjectType
from View.DomainView import RefreshShareCache

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import between, and_, or_
from sqlalchemy.orm import make_transient
import httplib
from uuid import uuid4
from Models.Database import db
from flask.module import Module
from Models.CloudStorge import *
from Models.Platform import *
from Tools.SqliteSession import ManualSession
from Tools import MailSender
import random
import datetime
import os
import os.path
from Tools.APIException import SystemErrorCode, APIException, DataErrorCode, AuthErrorCode, HandleStatusErrorCode
from flask import request
from flask import Flask, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from Tools.DataPaser import output_data, method_post_only, output_data_without_attribute, expandAttribute
from Tools.Permision import PermissionValidate, GetSessionId, refresh_user_permission, \
    Permission, objectOperatePermission
from Tools.GlobalVars import *
import hashlib
import io
from shutil import copy
from sqlalchemy import update
import re
import Image
import urllib
import urllib2




moudule = Module(__name__)

restfulApi = None

def route_config(app, api):
    app.register_module(moudule, url_prefix='/cloud')
    global restfulApi
    restfulApi = api


def getNipServerConfig():
    from Config import NIPServerBaseURL

    Connection = httplib.HTTPConnection
    Port = 80
    if NIPServerBaseURL.startswith('https'):
        Port = 443
        Connection = httplib.HTTPSConnection
    NIPServerBaseURL = NIPServerBaseURL[NIPServerBaseURL.index('://') + 3:]
    PortSpliterIndex = NIPServerBaseURL.find(':')
    if PortSpliterIndex != -1:
        sp = NIPServerBaseURL.split(':')
        Server = sp[0]
        Port = sp[1].split('/')[0]
    else:
        Server = NIPServerBaseURL
    return Connection, Port, Server


def getExtName(Name):
    reresult = re.compile(r'^.*?[.](?P<ext>tar\.gz|tar\.bz2|\w+)$').match(Name)
    if reresult is not None:
        return reresult.group('ext')
    return ''


def sum(list=[]):
    sum = 0
    for i in list:
        sum += int(i)
    return sum


def getSecurityObjectName(BaseDirObjectId, Name, IsCreate=False, ExcludeId=None):
    extName = getExtName(Name)
    pureName = Name
    if extName != '':
        pureName = Name[:len(Name) - len(extName) - 1]
    if extName != '':
        extName = '.' + extName
    if IsCreate:
        afterfix = ur''
    else:
        afterfix = ur' - 副本'
    condition = and_(Object.ParentId == BaseDirObjectId, Object.Name.like(pureName + '%' + extName))
    if ExcludeId is not None:
        condition = and_(condition, Object.Id != ExcludeId)
    names = db.session.query(Object.Name).filter(condition).all()
    if (Name,) not in names:
        return Name
    if afterfix != ur'':
        firstNewName = pureName + afterfix + extName
        if (firstNewName,) not in names:
            return firstNewName
    nameTemplate = pureName + afterfix + ur'(%d)' + extName
    for i in xrange(2, 99999):
        newName = nameTemplate % i
        if (newName,) not in names: break
    return newName

# 注册用户的账号状态
userUnverified = 0
userVerified = 1


@moudule.route('/modifyPassword', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['Password'])
@output_data
def modifyPassword():
    param = request.json_param
    try:
        Pwd = hashlib.md5(param[u'Password'].encode('utf-8')).hexdigest()
        user = User.query.filter_by(SessionId=request.sessionId, Password=Pwd).one()
        user.Password = hashlib.md5(param[u'NewPassword'].encode('utf-8')).hexdigest()
        s = param[u'NewPassword']
        if s.islower():
            level = 2
        else:
            level = 3
        if s.isdigit() or s.isalpha():
            level = 1
        user.Level = level
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'旧密码错误')
    db.session.commit()
    return user


@moudule.route('/modifyDescription', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def modifyDescription():
    param = request.json_param
    try:
        obj = Object.query.filter_by(Id=param[u'ObjectId']).one()
        obj.Camera = param[u'Camera']
        obj.Script = param[u'Script']
        obj.Tag = param[u'Tag']
        obj.Category_1 = param[u'Category_1']
        obj.Category_2 = param[u'Category_2']

        cur_time = datetime.datetime.now().strftime('%y-%m')
        portrait = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, 'temp', param[u'ObjImage'])
        destDir = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, cur_time)
        savePath = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, cur_time, param[u'ObjImage'])
        destPortrait = os.path.join(VISIT_FILE_FOLDER, G_ZONE_PIC, cur_time, param[u'ObjImage'])
        bHasPortrait = False
        left = param[u'Left']
        top = param[u'Top']
        right = param[u'Right']
        bottom = param[u'Bottom']
        bCut = False
        if right - left > 0 and bottom - top > 0:
            bCut = True
        if not os.path.exists(destDir):
            os.makedirs(destDir)
        if os.path.exists(portrait):
            if bCut:
                im = Image.open(portrait)
                width = im.size[0]
                height = im.size[1]
                box = (int(width * left), int(height * top), int(width * right), int(height * bottom))
                region = im.crop(box)
                region.save(savePath)
            else:
                copy(portrait, savePath)
            os.remove(portrait)
            bHasPortrait = True
        if bHasPortrait:
            obj.File.Path = destPortrait

        try:
            zi = ZoneItem.query.filter_by(ObjectId=obj.Id).one()
            zi.Intro = obj.Description
            if bHasPortrait:
                zi.Portrait = obj.File.Path
        except:
            pass

    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无此对象')
    db.session.commit()
    obj = expandAttribute(obj, ['File'])
    return obj


@moudule.route('/modifyBase', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def modifyBase():
    param = request.json_param
    try:
        obj = Object.query.filter_by(Id=param[u'ObjectId']).one()
        obj.Description = param[u'Description']

        try:
            zi = ZoneItem.query.filter_by(ObjectId=obj.Id).one()
            zi.Intro = obj.Description
        except:
            pass
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无此对象')
    db.session.commit()
    obj.Id
    return obj


@moudule.route('/modifyShareProperty', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def modifyShareProperty():
    param = request.json_param
    session = request.session

    try:
        obj = Object.query.filter_by(Id=param[u'ObjectId']).one()
        obj.BShare = param[u'BShare']

        if u'Price' in param:
            obj.Price = param[u'Price']

        if obj.Type is not 0:
            return APIException(SystemErrorCode.UnkonwnError, u'暂不支持非视频格式')

        if obj.BShare:
            try:
                item = db.session.query(ZoneItem).filter(and_(ZoneItem.DomainId == session['DomainId'],
                                                  ZoneItem.ObjectId == obj.Id)).one()
            except NoResultFound:
                item = ZoneItem(session['DomainId'], obj.Id, '')
                db.session.add(item)

            item.Type = ZoneItemType.Video
            item.Weight = 0
            item.Price = obj.Price
            item.ReferPrice = obj.ReferPrice
            item.BasePrice = obj.BasePrice
            item.SchemePrice = obj.SchemePrice
            item.ShotPrice = obj.ShotPrice
            item.ActorPrice = obj.ActorPrice
            item.MusicPrice = obj.MusicPrice
            item.AEPrice = obj.AEPrice
            item.Classical = 0
            item.Portrait = obj.File.Path
            item.Intro = obj.Description
        else:
            try:
                item = db.session.query(ZoneItem).filter(and_(ZoneItem.DomainId == session['DomainId'],
                                                              ZoneItem.ObjectId == obj.Id)).one()
                db.session.delete(item)
                CollectionVideo.query.filter_by(ZoneItemId=item.Id).delete()
            except NoResultFound:
                pass

        db.session.commit()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无此对象')

    return obj


@moudule.route('/modifyPriceProperty', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def modifyPriceProperty():
    param = request.json_param
    try:
        obj = Object.query.filter_by(Id=param[u'ObjectId']).one()

        if u'bp' in param:
            obj.BasePrice = float(param[u'bp'])
        if u'scp' in param:
            obj.SchemePrice = float(param[u'scp'])
        if u'shp' in param:
            obj.ShotPrice = float(param[u'shp'])
        if u'acp' in param:
            obj.ActorPrice = float(param[u'acp'])
        if u'mp' in param:
            obj.MusicPrice = float(param[u'mp'])
        if u'aep' in param:
            obj.AEPrice = float(param[u'aep'])
        obj.ReferPrice = obj.BasePrice + obj.SchemePrice + obj.ShotPrice + obj.ActorPrice + obj.MusicPrice + obj.AEPrice

        try:
            zi = ZoneItem.query.filter_by(ObjectId=obj.Id).one()
            zi.ReferPrice = obj.ReferPrice
            zi.BasePrice = obj.BasePrice
            zi.SchemePrice = obj.SchemePrice
            zi.ShotPrice = obj.ShotPrice
            zi.ActorPrice = obj.ActorPrice
            zi.MusicPrice = obj.MusicPrice
            zi.AEPrice = obj.AEPrice

        except NoResultFound:
            pass
        db.session.commit()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无此对象')
    obj.Id
    return obj


@moudule.route('/getIdentityCode', methods=['GET', 'POST'])
@output_data_without_attribute(['Password'])
@output_data
def getIdentityCode():
    param = request.json_param
    try:
        db.session.query(User.Id).filter(User.Email == param[u'Email']).one()
    except NoResultFound:
        try:
            ri = db.session.query(RegisterIdentity).filter(RegisterIdentity.Email == param[u'Email']).one()
        except NoResultFound:
            ri = RegisterIdentity(param[u'Email'])
            db.session.add(ri)
        ri.IdentityCode = random.randint(100000, 999999)
        ri.CreateTime = datetime.datetime.now()
        body = "欢迎注册！您的验证码为：" + str(ri.IdentityCode) + "，请在10分钟内完成注册流程，防止验证码过期";

        from Main import app

        try:
            MailSender.send_mail(app, body, "", [param[u'Email']], "注册验证码")
        except:
            return {"bSend": False}
        db.session.commit()
        # return {"bSend": True, "IdentityCode": ri.IdentityCode}
        return {"bSend": True, "IdentityCode": 0} #不能把验证码返回
    return APIException(SystemErrorCode.UnkonwnError, u'邮箱已被占用')


@moudule.route('/checkName', methods=['GET', 'POST'])
@output_data_without_attribute(['Password'])
@output_data
def checkName():
    param = request.json_param
    try:
        db.session.query(User.Id).filter(User.Email == param[u'Email']).one()
    except NoResultFound:
        return {"bValidName": True}
    return {"bValidName": False}


@moudule.route('/search', methods=['GET', 'POST'])
@output_data_without_attribute(['MD5', 'Password'])
@output_data
def search():
    param = request.json_param
    searchPhase = "%" + param[u'SearchKeyword'] + "%"

    # if param[u'SearchKeyword'] == '':
    #     return {'domain': [], 'video': []}

    if param[u'SearchType'] == 'all':
        domain = Domain.query.filter(and_(Domain.CompanyName.like(searchPhase), Domain.IsService == 1)).all()
        video = db.session.query(ZoneItem).join(Object, Object.Id == ZoneItem.ObjectId)\
            .filter(or_(Object.Name.like(searchPhase), Object.Tag.like(searchPhase))).all()
        return {'domain': domain, 'video': video}
    elif param[u'SearchType'] == 'producer':
        domain = Domain.query.filter(and_(Domain.CompanyName.like(searchPhase), Domain.IsService == 1)).all()
        rf = ResourceShare.query.filter_by(ResourceId=param['reqId'], ResourceType='r').all()
        domain = expandAttribute(domain, [])
        for d in domain:
            d['bSelect'] = False
            for v in rf:
                if v.ShareDomainId == 0:
                    break
                if d['Id'] == v.ShareDomain.Id:
                    d['bSelect'] = True
                    break
        return {'domain': domain}


# 修改用户信息
@moudule.route('/modifyUserInfo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def modifyUserInfo():
    session = request.session
    param = request.json_param
    userId = session['UserId']
    user = User.query.filter_by(Id=userId).one()
    if user.Domain.Status != 2:
        if u'NickName' in param:
            user.Domain.CompanyName = user.NickName
        if u'CellPhone' in param:
            user.Domain.CompanyCelPhone = user.CellPhone
    if u'RealName' in param:
        user.RealName = param[u'RealName']
    if u'NickName' in param:
        user.NickName = param[u'NickName']
    if u'CellPhone' in param:
        user.CellPhone = param[u'CellPhone']
    if u'CompanyAddr' in param:
        user.Domain.CompanyAddr = param[u'CompanyAddr']
    if u'CompanyLicense' in param:
        user.Domain.CompanyLicense = param[u'CompanyLicense']
    if u'CompanyName' in param:
        user.Domain.CompanyName = param[u'CompanyName']
    if u'CompanyEmail' in param:
        user.Domain.CompanyEmail = param[u'CompanyEmail']
    if u'CompanyPhone' in param:
        user.Domain.CompanyPhone = param[u'CompanyPhone']
    if u'CompanyFax' in param:
        user.Domain.CompanyFax = param[u'CompanyFax']
    if u'DomainName' in param:
        user.Domain.DomainName = param[u'DomainName']
    if u'CompanyCelPhone' in param:
        user.Domain.CompanyCelPhone = param[u'CompanyCelPhone']
    if u'Portrait' in param:
        left = param[u'left']
        top = param[u'top']
        right = param[u'right']
        bottom = param[u'bottom']
        bCut = False
        if right - left > 0 and bottom - top > 0:
            bCut = True
        cur_time = datetime.datetime.now().strftime('%y-%m')
        portrait = os.path.join(G_UPLOAD_FILE_FLODER, G_USER_PORTRAIT, 'temp', param[u'Portrait'])
        destDir = os.path.join(G_UPLOAD_FILE_FLODER, G_USER_PORTRAIT, cur_time)
        savePath = os.path.join(G_UPLOAD_FILE_FLODER, G_USER_PORTRAIT, cur_time, param[u'Portrait'] + '.png')
        destPortrait = os.path.join(VISIT_FILE_FOLDER, G_USER_PORTRAIT, cur_time, param[u'Portrait'] + '.png')
        if not os.path.exists(destDir):
            os.makedirs(destDir)
        if os.path.exists(portrait):
            im = Image.open(portrait)
            width = im.size[0]
            height = im.size[1]
            if bCut:
                box = (int(width * left), int(height * top), int(width * right), int(height * bottom))
                region = im.crop(box)
                region.save(savePath)
            else:
                if width >= height:
                    box = (0, 0, height, height)
                else:
                    box = (0, 0, width, width)
                region = im.crop(box)
                region.save(savePath)
                # copy(portrait, destDir)
            os.remove(portrait)
            delPortrait = G_STATIC_FOLDER + user.Domain.Portrait
            try:
                if os.path.exists(delPortrait):
                    os.remove(delPortrait)
            except:
                pass
            user.Domain.Portrait = destPortrait
    db.session.commit()
    return user


@moudule.route('/getUserInfo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['Password'])
@output_data
def getUserInfo():
    session = request.session
    UserId = session['UserId']
    user = User.query.filter_by(Id=UserId).one()
    return user

@moudule.route('/getAllUser', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getAllUser():
    user = User.query.all()
    return user

@moudule.route('/getUnverifiedUserInfo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['Password'])
@output_data
def getUnverifiedUserInfo():
    users = User.query.filter_by(Status=userUnverified).all()
    return users


@moudule.route('/verifiedUser', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def verifiedUser():
    param = request.json_param
    try:
        user = User.query.filter_by(Id=param[u'UserId']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'没有该用户')
    if param[u'Pass']:
        body = "欢迎注册！您的账号已经通过验证，登录网站立即体验"
    else:
        body = param[u'Description']

    from Main import app

    try:
        MailSender.send_mail(app, body, "", [param[u'Email']], "账号审核结果")
    except:
        return APIException(SystemErrorCode.UnkonwnError, u'通知邮件发送失败，请查看服务器状态')

    if param[u'Pass']:
        user.Status = userVerified
    else:
        Object.query.filter_by(OwnerUserId=user.Id).delete()
        Role.query.filter_by(CreatorId=user.Id).delete()
        Domain.query.filter_by(OwnerUserId=user.Id).delete()
        db.session.delete(user)
    db.session.commit()
    return {"verifiedUser": True}


@moudule.route('/deleteUser', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def deleteUser():
    param = request.json_param
    try:
        user = User.query.filter_by(Id=param[u'UserId']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'没有该用户')

    Object.query.filter_by(OwnerUserId=user.Id).delete()
    Role.query.filter_by(CreatorId=user.Id).delete()
    Domain.query.filter_by(OwnerUserId=user.Id).delete()
    db.session.delete(user)
    db.session.commit()
    return {"deleteUser": True}


@moudule.route('/retrieveSession', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def retrieveSession():
    session = request.session
    result = {}
    try:
        user = User.query.filter_by(Id=session['UserId']).one()
    except NoResultFound:
        return result
    result[u'UserId'] = session['UserId']
    result[u'IsService'] = session['IsService']
    result[u'NickName'] = session['NickName']
    result[u'DBToken'] = session['DBToken']
    result[u'DomainId'] = user.DomainId
    result[u'ExpireTime'] = user.Domain.ExpireTime
    user = User.query.filter_by(Id=session['UserId']).one()
    result[u'DomainInUse'] = (user.Domain.Status != DomainStatus.init)
    result[u'DomainPrepare'] = user.Domain.Status == DomainStatus.review
    tempRights = {}
    if len(user.Roles) != 0:
        rolesId = []
        for role in user.Roles:
            rolesId.append(role.Id)
        roleR = RoleRight.query.filter(RoleRight.RoleId.in_(rolesId)).all()
        for r in roleR:
            tempRights[r.RightId] = 0
            tempRights[r.RightId] |= r.Checked

    rights = Right.query.all()
    userRights = {}
    for right in rights:
        if right.Id in tempRights:
            userRights[right.Identity] = tempRights[right.Id]
    result[u'UserRights'] = userRights
    return result


@moudule.route('/register', methods=['GET', 'POST'])
@output_data_without_attribute(['Password'])
@output_data
def register():
    param = request.json_param
    # 验证码校验
    identityCode = param[u'IdentityCode']
    try:
        identity = db.session.query(RegisterIdentity).filter(RegisterIdentity.Email == param[u'UserName']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'请输入正确的验证码并检查邮箱地址是否输入正确')
    duration = datetime.datetime.now() - identity.CreateTime
    if duration > datetime.timedelta(minutes=10):
        return APIException(SystemErrorCode.UnkonwnError, u'验证码已过期，请重新获取验证码')
    if identityCode != identity.IdentityCode:
        return APIException(SystemErrorCode.UnkonwnError, u'验证码错误')

    try:
        db.session.query(User.Id).filter(User.Email == param[u'UserName']).one()
    except NoResultFound:
        user = User(None, param[u'UserName'], param[u'UserName'])
        user.Password = param[u'Password']
        user.DomainName = param[u'UserName']
        user.Status = userVerified
        user.type = 0
        user.SessionId = ''
        s = user.Password
        if s.islower():
            level = 2
        else:
            level = 3
        if s.isnumeric() or s.isalpha():
            level = 1
        user.Level = level
        #在未有审核前，直接通过
        user.Status = userVerified
        user.type = 0
        db.session.add(user)
        db.session.flush()

        #家庭组创建，暂时不校验共享云名称，不同用户可以含有共同的共享云名称
        # if Domain.query.filter_by(DomainName=param[u'DomainName']).count() > 0:
        #     return APIException(DataErrorCode.DomainNameExist, u'域名已被占用')
        domain = Domain(param[u'UserName'], user.Id)
        domain.DefaultStorageSize = 1024 * 1024 * 1024 * 2
        domain.UsedSize = 0
        #公司注册
        if u'CompanyName' in param:
            domain.CompanyName = param[u'CompanyName']
            domain.CompanyAddr = param[u'Address']
            domain.IsService = 1
            domain.DefaultStorageSize = 1024 * 1024 * 1024 * 5
            domain.CompanyLicense = param[u'License']
            user.RealName = param[u'RealName']
            user.CellPhone = param[u'CellPhone']
            domain.Status = DomainStatus.use
        db.session.add(domain)
        db.session.flush()
        domain.Users.append(user)
        role = Role(u'超级管理员', None, user.Id, 1)
        domain.Roles.append(role)
        user.Roles.append(role)
        db.session.add(role)
        rights = Right.query.all()
        for right in rights:
            if right.Leaf:
                roleRight = RoleRight(right.Id, role.Id, 1)
                db.session.add(roleRight)

        rootobject = Object(param[u'UserName'], 1, 2, None, user.Id, user.Id, None)
        db.session.add(rootobject)
        #注册成功，清理验证码记录
        RegisterIdentity.query.filter_by(Email=param[u'UserName']).delete()
        db.session.commit()
        return {"bRegister": True}
    return APIException(SystemErrorCode.UnkonwnError, u'邮箱已被占用')


@moudule.route('/login', methods=['GET', 'POST'])
@output_data_without_attribute(['Password'])
@output_data
def login():
    param = request.json_param
    if u'DomainName' not in param:
        if u'UserName' not in param:
            try:
                openId = session['openId']
                user = db.session.query(User).filter(User.WeiXinOpenId == openId).one()
            except:
                return APIException(SystemErrorCode.UnkonwnError, u'用户名或密码错误')
        else:
            try:
                user = db.session.query(User).filter(User.Email == param[u'UserName'], User.Password == param[u'Password']).one()
            except NoResultFound:
                return APIException(SystemErrorCode.UnkonwnError, u'用户名或密码错误')
    else:
        try:
            user = db.session.query(User).join(Domain, User.DomainId == Domain.Id)\
                .filter(Domain.DomainName == param[u'DomainName'])\
                .filter(or_(User.DomainName == param[u'UserName'], User.NickName == param[u'UserName']))\
                .filter(User.Password == param[u'Password']).one()
        except NoResultFound:
            return APIException(SystemErrorCode.UnkonwnError, u'用户名或密码错误')
    if user.Status == userUnverified:
        return APIException(SystemErrorCode.UnkonwnError, u'该用户账号尚未通过审核')
    ms = ManualSession()
    our_session = ms.open_session(create=True)
    if user.SessionId is not None and user.SessionId != our_session.sid:
        ms.close_session(sid=user.SessionId)
    user.SessionId = our_session.sid
    user.LastLoginTime = datetime.datetime.now()
    db.session.commit()
    our_session["UserId"] = user.Id
    our_session["IsService"] = user.Domain.IsService
    our_session["CompanyName"] = user.Domain.CompanyName
    our_session["DBToken"] = our_session.sid
    our_session["NickName"] = user.NickName
    our_session["DomainName"] = user.DomainName
    our_session["DomainId"] = user.DomainId

    tempRights = {}
    if len(user.Roles) != 0:
        rolesId = []
        for role in user.Roles:
            rolesId.append(role.Id)
        result = RoleRight.query.filter(RoleRight.RoleId.in_(rolesId)).all()
        for r in result:
            tempRights[r.RightId] = 0
            tempRights[r.RightId] |= r.Checked

    rights = Right.query.all()
    userRights = {}
    for right in rights:
        if right.Id in tempRights:
            userRights[right.Identity] = tempRights[right.Id]
    respObj = {"DBToken": our_session.sid, "IsService": user.Domain.IsService, "NickName": user.NickName, "UserId": user.Id,
               "CompanyName": user.Domain.CompanyName, "DomainId": user.DomainId, "UserRights": userRights,
               "DomainInUse": user.Domain.Status != DomainStatus.init}
    from Main import api
    from flask.ext.restful import unpack

    data, code, headers = unpack(respObj)
    resp = api.make_response(data, code, headers=headers)
    resp.set_cookie("DBToken", our_session.sid, secure=True)
    resp.set_cookie("DBToken", our_session.sid, secure=False)
    return resp


@moudule.route('/logout', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def logout():
    session = request.session
    ms = ManualSession()
    user = User.query.filter_by(Id=session['UserId']).one()
    user.LeastTime = datetime.datetime.now()
    db.session.commit()
    ms.close_session(session)
    from Main import api
    resp = api.make_response('', 200, headers='')
    resp.set_cookie("DBToken", '', expires=-1)
    return resp

@moudule.route('/getDBList', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def getDBList():
    session = request.session
    UserId = session['UserId']
    user = User.query.filter_by(Id=UserId).one()
    rootobject = None
    try:
        rootobject = Object.query.filter_by(ParentId=None, OwnerUserId=UserId).one()
    except NoResultFound:
        pass
    userdict = user.__dict__
    domain = user.Domain.__dict__
    domain['RootObject'] = Object.query.filter_by(ParentId=None, OwnerUserId=user.Domain.OwnerUserId).one()
    userdict['Domain'] = domain

    if rootobject is not None:
        userdict["RootObject"] = rootobject
    shares = StorageShare.query.filter_by(ObjectOwnerDomainId=session['DomainId']).all()

    c1 = Category.query.filter_by(Level=1).all()
    c2 = Category.query.filter_by(Level=2).all()

    tags = db.session.query(Tag).filter(Tag.UserId.is_(None)).all()
    DBListInfo = {"User": userdict, "Shares": shares, "Category_1": c1, "Category_2": c2, "Tags": tags}
    return DBListInfo


@moudule.route('/getShareUsers', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['Roles'])
@output_data
def getShareUsers():
    session = request.session
    ss = db.session.query(StorageShare.ObjectOwnerDomainId.distinct(), Domain)\
        .join(Domain, Domain.Id == StorageShare.ObjectOwnerDomainId)\
        .filter(StorageShare.DomainId == session['DomainId']).all()
    domains = []
    for k in ss:
        domains.append(k[1])
    return domains


@moudule.route('/getShares', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['CreatorUser', 'Groups', 'Users', 'Roles', 'MD5'])
@output_data
def getShares():
    session = request.session
    param = request.json_param
    result = StorageShare.query.filter_by(ObjectOwnerDomainId=param[u'ShareDomainId'],
                                          DomainId=session['DomainId']).all()
    return result


@moudule.route('/getMyShares', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def getMyShares():
    session = request.session
    param = request.json_param
    UserId = session['UserId']
    results = []
    ss = db.session.query(StorageShare.ObjectId.distinct(), Object)\
        .join(Object, Object.Id == StorageShare.ObjectId)\
        .filter(StorageShare.ObjectOwnerDomainId == session['DomainId']).all()
    objects = []
    for k in ss:
        objects.append(k[1])
    return {'Items': objects}


@moudule.route('/childObjects', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def childObjects():
    session = request.session
    param = request.json_param
    UserId = objectOperatePermission(param['Id'], session['UserId'], 'storage', 'read')
    IsDeep = False
    try:
        IsDeep = param[u'IsDeep']
    except:
        pass
    if IsDeep:
        try:
            lr = Object.query.filter_by(OwnerUserId=UserId, Id=param[u'Id']).one()
        except:
            return APIException(SystemErrorCode.UnkonwnError, u'目标目录不存在或没有访问权限')
        return {'Items': Object.query.filter(
            and_(Object.OwnerUserId == UserId, between(Object._Left_, lr._Left_, lr._Right_))).all()}
    else:
        page = 1
        per_page = 20
        try:
            page = param[u'Page']
            per_page = param[u'PageStep']
        except:
            pass
        if u'SearchKeyword' in param:
            searchPhase = "%" + param[u'SearchKeyword'] + "%"
            pagination = Object.query.filter(and_(Object.OwnerUserId == UserId, Object.Name.like(searchPhase))).paginate(page, per_page)
        else:
            pagination = Object.query.filter(and_(Object.OwnerUserId == UserId, Object.ParentId == param[u'Id'])).paginate(page, per_page)
        return {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
                'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
                'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}


# 移动对象接口
@moudule.route('/moveObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def moveObject():
    session = request.session
    param = request.json_param
    UserId = objectOperatePermission(param['DestId'], session['UserId'], 'storage', 'write')
    dest = Object.query.filter_by(Id=param['DestId'], OwnerUserId=UserId, FileId=None).one()
    src = Object.query.filter_by(Id=param['SrcId'], OwnerUserId=UserId).one()
    src_left = src._Left_
    src_right = src._Right_
    dest_left = dest._Left_
    dest_right = dest._Right_
    src_diff = (src_right - src_left)
    VERY_BIG_INT = 9023372036854775807
    if src_left < dest_left:
        dest_new_left = dest_left - src_diff - 1
        src_new_diff = dest_new_left - src_left + 1
        dest_new_right = dest_right
        between_diff = -(src_diff + 1)
        between_cond = Object._Left_.between(src_right, dest_left - 2)
        between_cond2 = Object._Left_.between(src_right + VERY_BIG_INT, dest_left - 2 + VERY_BIG_INT)
    else:
        dest_new_left = dest_left
        src_new_diff = dest_new_left - src_left + 1
        dest_new_right = src_right + src_new_diff + 1
        between_diff = src_diff + 1
        between_cond = Object._Right_.between(dest_right + 2, src_left)
        between_cond2 = Object._Right_.between(dest_right + 2 + VERY_BIG_INT, src_left + VERY_BIG_INT)
    src.Name = getSecurityObjectName(dest.Id, src.Name, True)
    Object.query.filter(between_cond, Object.OwnerUserId == UserId).update(
        {'_Left_': Object._Left_ + VERY_BIG_INT, '_Right_': Object._Right_ + VERY_BIG_INT},
        synchronize_session=False)  # bigint maxvalue:9223372036854775807
    Object.query.filter(Object._Left_ >= src_left, Object._Left_ <= src_right, Object.OwnerUserId == UserId).update(
        {'_Left_': Object._Left_ + src_new_diff, '_Right_': Object._Right_ + src_new_diff})
    Object.query.filter(between_cond2, Object.OwnerUserId == UserId).update(
        {'_Left_': Object._Left_ - VERY_BIG_INT + between_diff,
         '_Right_': Object._Right_ - VERY_BIG_INT + between_diff}, synchronize_session=False)
    dest._Left_ = dest_new_left
    dest._Right_ = dest_new_right
    src.ParentId = dest.Id
    db.session.commit()
    src.Id
    return {"movedObject": src}


# 深拷贝接口
@moudule.route('/copyObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def copyObject():
    session = request.session
    param = request.json_param
    srcUserId = objectOperatePermission(param['SrcId'], session['UserId'], 'storage', 'write')
    destUserId = objectOperatePermission(param['DestId'], session['UserId'], 'storage', 'write')

    dest = Object.query.filter_by(Id=param[u'DestId'], OwnerUserId=destUserId, FileId=None).one()
    src = Object.query.filter_by(Id=param[u'SrcId'], OwnerUserId=srcUserId).one()
    dest_right = dest._Right_
    src_left = src._Left_
    objects = Object.query.filter(between(Object._Left_, src._Left_, src._Right_),
                                  Object.OwnerUserId == srcUserId).all()

    indexedObjects = {}  #建立索引，以便构建新树
    for obj in objects:
        if obj.ParentId not in indexedObjects:
            indexedObjects[obj.ParentId] = []
        indexedObjects[obj.ParentId].append(obj)
    sizelist = []
    src_dest_diff = (dest_right - src_left)
    with db.session.no_autoflush:
        for x in objects:
            db.session.expunge(x)
            make_transient(x)
            x._Left_ = x._Left_ + src_dest_diff
            x._Right_ = x._Right_ + src_dest_diff
            x.OwnerUserId = destUserId
            if x.Size is not None:
                sizelist.append(x.Size)
            if x.File is not None:
                x.File.RefCount += 1
            db.session.add(x)
        Object.query.filter(Object._Left_ >= dest._Right_, Object.OwnerUserId == destUserId).update(
            {'_Left_': Object._Left_ + 2 * len(objects)})
        Object.query.filter(Object._Right_ >= dest._Right_, Object.OwnerUserId == destUserId).update(
            {'_Right_': Object._Right_ + 2 * len(objects)})
        sumsize = int(sum(sizelist))
        userinfo = User.query.filter_by(Id=destUserId).one()
        surplus = userinfo.Domain.DefaultStorageSize + userinfo.Domain.ExtendStorageSize - userinfo.Domain.UsedSize
        if sumsize > surplus:
            return APIException(DataErrorCode.NoStorageSize, u'存储空间不足', request.path)
        root = indexedObjects[src.ParentId][0]
        dest.Children.append(root)
        root.Name = getSecurityObjectName(dest.Id, root.Name)
        ids = {root.Id: root}
        while len(ids) != 0:
            id, parentObj = ids.popitem()  #重建树形结构
            if id in indexedObjects:
                for obj in indexedObjects[id]:
                    parentObj.Children.append(obj)
                    if obj.File is None:
                        ids[obj.Id] = obj
                    else:
                        obj.Id = None
            parentObj.Id = None  #清空ID以便插入
        u = User.query.filter(User.Id == destUserId).one()
        u.Domain.UsedSize = u.Domain.UsedSize + sumsize
    db.session.commit()
    return objects


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'zip', 'rar', 'mp4', 'mpg', 'mpeg', 'rar', 'rp',
                          'rmvb', 'doc', 'vod', 'mov', 'xls', 'docx', 'xlsx', 'psd', 'mp3', 'rm', 'flv', 'avi', 'mod', 'wmv', '3gp', 'mp3', 'mkv'])

VIDEO_TYPE = set(['mp4', 'mpg', 'mpeg', 'rp', 'rmvb', 'vod', 'mov', 'rm', 'flv', 'avi', 'mod', 'wmv', '3gp', 'mp3', 'mkv'])
IMAGE_TYPE = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
DOCUMENT_TYPE = set(['txt', 'pdf', 'doc', 'docx', 'xlsx', 'xls','wmv'])


def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS):
    return '.' in filename and \
           (getExtName(filename).lower() in allowed_extensions or allowed_extensions == '*')


def calMd5(afile):
    m = hashlib.md5()
    file = io.FileIO(afile, 'r')
    bytes = file.read(1024)
    while (bytes != b''):
        m.update(bytes)
        bytes = file.read(1024)
    file.close()
    md5value = m.digest()
    return md5value


#注册上传文件接口
@moudule.route('/uploadLicenseFile', methods=['GET', 'POST'])
@output_data
def uploadLicenseFile():
    try:
        admin = User.query.filter_by(Email="admin@HT.com").one()
    except NoResultFound:
        return APIException(SystemErrorCode.NonPermissionCreate, u'对不起，系统故障，无法上传证件，请联系客服人员', request.path)
    return uploadFile_common(admin.Id)


#上传文件接口
@moudule.route('/uploadFile', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def uploadFile():
    session = request.session
    request.json_param = param = request.values
    UserId = objectOperatePermission(param['Id'], session['UserId'], 'storage', 'write')
    return uploadFile_common(UserId)


#查询文件信息接口
@moudule.route('/getFileInfo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getFileInfo():
    param = request.json_param
    session = request.session
    UserId = session['UserId']
    try:
        fileInfo = FileCache.query.filter_by(ClientFileName=param[u'IdentityName']).one()
    except NoResultFound:
        result = verify_uploadFile()
        if result == 1:
            return APIException(SystemErrorCode.NonPermissionUpload, u'没有权限上传', param[u'FileName'])
        if result == 2:
            return APIException(SystemErrorCode.NonSupportFileType, u'禁止上传的文件类型', param[u'FileName'])
        if result == 3:
            return APIException(DataErrorCode.NoStorageSize, u'存储空间不足', param[u'FileName'])
        fileInfo = FileCache(param[u'IdentityName'], str(uuid4()), param[u'FileSize'], UserId, param[u'FileName'])
        db.session.add(fileInfo)
        db.session.commit()
        fileInfo.Id
    return fileInfo


#上传文件接口
@moudule.route('/smartUpload', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def smartUpload():
    request.json_param = param = request.values
    session = request.session
    UserId = session['UserId']
    try:
        fileInfo = FileCache.query.filter_by(Id=param[u'identityName']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无文件续传信息')
    response = fileInfo
    for index in request.files:
        task = request.files[index]
        filePath = os.path.join(G_UPLOAD_FILE_FLODER, fileInfo.ServerFileName)
        if os.path.exists(filePath):
            curSize = os.path.getsize(filePath)
            if curSize + long(param[u'size']) > fileInfo.TotalSize:
                return APIException(SystemErrorCode.UnkonwnError, u'文件大小溢出异常')
            if curSize != long(param[u'start']):
                return APIException(SystemErrorCode.UnkonwnError, u'文件位置不匹配')
        filePathTemp = filePath + "temp"
        task.save(filePathTemp)
        fp = open(filePath, 'ab')
        fpTemp = open(filePathTemp, 'rb')
        fp.write(fpTemp.read())
        fpTemp.close()
        #fp.write(task.stream.getvalue())
        fp.close()
        fileInfo.Size = os.path.getsize(filePath)
        if fileInfo.Size >= fileInfo.TotalSize:
            response.data = smartUpload_save(UserId, fileInfo, filePath)
    db.session.commit()
    fileInfo.Id
    return response
#取得Object信息接口
@moudule.route('/getObject', methods=['GET', 'POST'])
@output_data_without_attribute(['MD5'])
@output_data
def getobject():
    param = request.json_param
    id = param[u'Id']
    obj = Object.query.filter_by(Id=id).one()
    UserId = obj.OwnerUserId
    user = User.query.filter_by(Id=UserId).one()
    result = {}
    result[u'obj'] = obj
    result[u'user'] = user
    return result

#打开播放页接口
@moudule.route('/openFile', methods=['GET', 'POST'])
@output_data
def openFile():
    Id = request.values[u'Id']
    param = request.json_param
    obj = Object.query.filter_by(Id=Id).one()
    if obj.File is None:
        return APIException(40400, u'非文件对象不能下载')
    from Main import app

    resp = app.make_response((''))
    resp.headers['X-Accel-Redirect'] = '/' + os.path.join(G_UPLOAD_FILE_FLODER_REL, obj.File.Path)
    resp.headers['Content-Type'] = ''
    resp.headers['Content-Disposition'] = ('attachment; filename=' + obj.Name).encode('utf8')
    return resp

#下载文件接口
@moudule.route('/downloadFile', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def downloadFile():
    session = request.session
    param = request.json_param
    Id = param[u'Id']
    objectOperatePermission(Id, session['UserId'], param[u'Context'], 'download')
    obj = Object.query.filter_by(Id=Id).one()
    if obj.File is None:
        return APIException(40400, u'非文件对象不能下载')
    from Main import app

    resp = app.make_response((''))
    resp.headers['X-Accel-Redirect'] = '/' + os.path.join(G_UPLOAD_FILE_FLODER_REL, obj.File.Path)
    resp.headers['Content-Type'] = ''
    resp.headers['Content-Disposition'] = ('attachment; filename=' + obj.Name).encode('utf8')
    return resp


#下载文件接口
@moudule.route('/getDownloadPermission', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def downloadPermission():
    session = request.session
    param = request.json_param
    objectOperatePermission(param[u'Id'], session['UserId'], param[u'Context'], 'download')
    return {}


def createDirObject(DestId, UserId, Name=u'新建文件夹'):
    destdirinfo = Object.query.filter_by(Id=DestId).one()
    if UserId == destdirinfo.OwnerUserId:
        Object.query.filter(Object._Left_ >= destdirinfo._Right_, Object.OwnerUserId == UserId).update(
            {'_Left_': Object._Left_ + 2})
        Object.query.filter(Object._Right_ >= destdirinfo._Right_, Object.OwnerUserId == UserId).update(
            {'_Right_': Object._Right_ + 2})
        p = Object(getSecurityObjectName(DestId, Name, True), destdirinfo._Right_ - 2, destdirinfo._Right_ - 2 + 1,
                   destdirinfo.Id, UserId, UserId, None)
        db.session.add(p)
        return p
    else:
        return APIException(SystemErrorCode.NonPermissionCreate, u'没有权限进行创建', request.path)


#创建目录信息接口
@moudule.route('/createDir', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def createDir():
    session = request.session
    param = request.json_param
    UserId = objectOperatePermission(param['DestId'], session['UserId'], 'storage', 'write')
    dir = createDirObject(param[u'DestId'], UserId, param[u'Name'])
    db.session.commit()
    dir.Id
    return dir


class ExecuteStatus(IntEnum):
    UpLoading, TransCoding, UpLoadComplete = range(1, 4)


    # UpLoading, UpLoadComplete = 1,3


#创建素材
@moudule.route('/createClip', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def createClip():
    session = request.session
    param = request.json_param
    UserId = objectOperatePermission(param['Id'], session['UserId'], 'storage', 'write')
    clip = createDirObject(param[u'DestId'], UserId, param[u'Name'])
    clip.Status = ExecuteStatus.UpLoading.value  #TODO (.value 代表取整形，.name 代表取字符串)
    db.session.commit()
    clip.Id
    return clip


#创建完成
@moudule.route('/createClipDone', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def createClipDone():
    session = request.session
    param = request.json_param
    UserId = objectOperatePermission(param['Id'], session['UserId'], 'storage', 'write')
    clipinfo = Object.query.filter_by(Id=param[u'Id']).one()
    if UserId == clipinfo.OwnerUserId:
        if clipinfo.Status == ExecuteStatus.UpLoading.value:
            clipinfo.Status = ExecuteStatus.UpLoadComplete.value
        else:
            return APIException(DataErrorCode.StatusError, u'状态错误，执行中断')
    else:
        return APIException(SystemErrorCode.NonPermissionHandle, u'没有权限执行此操作', request.path)
    db.session.commit()
    return clipinfo


#创建文件信息接口
@moudule.route('/createFile', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def createFile():
    session = request.session
    param = request.json_param
    UserId = objectOperatePermission(param['Id'], session['UserId'], 'storage', 'write')
    try:
        destdirinfo = Object.query.filter_by(Id=param[u'DestId']).one()
        fileinfo = File.query.filter_by(Id=param[u'FileId'], MD5=param[u'MD5']).one()
        user = User.query.filter_by(Id=UserId).one()
    except NoResultFound:
        return APIException(DataErrorCode.NoRecord, "目标文件夹，或目标文件不存在")
    if UserId == destdirinfo.OwnerUserId and param['MD5'] == fileinfo.MD5:
        Object.query.filter(Object._Left_ >= destdirinfo._Right_, Object.OwnerUserId == UserId).update(
            {'_Left_': Object._Left_ + 2})
        Object.query.filter(Object._Right_ >= destdirinfo._Right_, Object.OwnerUserId == UserId).update(
            {'_Right_': Object._Right_ + 2})
        p = Object(getSecurityObjectName(destdirinfo.Id, param[u'Name']))
        p.FileId = param[u'FileId']
        p.Size = fileinfo.Size
        p._Left_ = destdirinfo._Right_ - 2
        p._Right_ = destdirinfo._Right_ - 2 + 1
        p.ParentId = destdirinfo.ParentId
        p.OwnerUserId = p.CreatorUserId = UserId
        user.Domain.UsedSize += p.Size
    else:
        return APIException(SystemErrorCode.NonPermissionCreate, u'没有权限进行创建', request.path)
    db.session.add(p)
    db.session.commit()
    p.Id
    return p


#修改对象名接口
@moudule.route('/renameObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def renameObject():
    session = request.session
    param = request.json_param
    UserId = objectOperatePermission(param['Id'], session['UserId'], 'storage', 'write')
    c = Object.query.filter_by(Id=param[u'Id']).one()
    if UserId == c.OwnerUserId:
        if c.Name != param[u'Name']:
            c.Name = getSecurityObjectName(c.ParentId, param[u'Name'], True, c.Id)
    else:
        return APIException(SystemErrorCode.NotAllowAmend, u'不允许修改', request.path)
    db.session.commit()
    c.Id
    return c

def delFileUrl(FilePath, filecode):  # 删除转码网站的文件
    # from urllib2 import Http
    # h = Http()
    # headers = {'Connection':'keep-alive'}
    # h.request('http://localhost:8989/','GET',None,headers=headers)

    param = urllib.urlencode({'action': 'delete', 'filecode': filecode, 'filepath': FilePath, 'perID': '73d2428effef619d51d8bcca966f7d98'})
    ulrpath = "http://123.57.157.64:8080/query.aspx?%s" % param
    rlt = ''
    try:
        rlt = urllib2.urlopen(ulrpath).read()   # 需要转码网站处理
    except urllib2.HTTPError,e:
       print e.code
    except urllib2.URLErrror,e:
        print str(e)
    donerlt = 'Delete File Done'
    if rlt.find(donerlt) >= 0:
        return True

    return False

def delFileLocal(FilePath, filecode):
    fileAllPath = G_STATIC_FOLDER + FilePath
    fileAllPath = os.path.normpath(fileAllPath)
    if os.path.isdir(fileAllPath):
        return False
    if not os.path.exists(fileAllPath):
        return True

    # os.remove(fileAllPath)
    return True


def delFile(filepath, videoFilePath, filecode):
    # regex = re.compile(
    # r'^(?:http|ftp)s?://' # http:// or https://
    # r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    # r'localhost|' #localhost...
    # r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    # r'(?::\d+)?' # optional port
    # r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    regex7 = re.compile(r'^http://7xl6yy.com1.z0.glb.clouddn.com?', re.IGNORECASE)
    regexserver = re.compile(r'^http://123.57.157.64:8080?', re.IGNORECASE)

    Done = True
    # 删除图标文件
    if regex7.match(filepath):
        if not delFileUrl(filepath,filecode):
            Done = False
    elif regexserver.match(filepath):
        if not delFileUrl(filepath,filecode):
            Done = False
    else:
        if not delFileLocal(filepath,filecode):
            Done = False

    # 删除视频文件
    if regex7.match(videoFilePath):
        if not delFileUrl(videoFilePath,filecode):
            Done = False
    elif regexserver.match(videoFilePath):
        if not delFileUrl(videoFilePath,filecode):
            Done = False
    else:
        if not delFileLocal(videoFilePath,filecode):
            Done = False

    return Done


#删除File
@moudule.route('/delTrashFile', methods=['GET'])
@output_data
def delTrashFile():
    param = request.json_param
    if 'permissionId' not in param:
        return restfulApi.make_response({'bResult': False, 'error': u'not authorized call!'}, 200, headers='')
    if param['permissionId'] != 'af5d3597ca239f6386f55729ced6efe6':
        return restfulApi.make_response({'bResult': False, 'error': u'not authorized call!'}, 200, headers='')

    try:
        allFile = File.query.filter(File.RefCount <= 0).all()
    except NoResultFound:
        return restfulApi.make_response({'bResult': True, 'error': u'not need clear!'}, 200, headers='')

    timenow = datetime.datetime.now()
    timeinterval = datetime.timedelta(days=7)
    for itor in allFile:
        duration = timenow - itor.DelTime
        if duration > timeinterval:
            if delFile(itor.Path, itor.VideoFile, itor.FileCode):
                db.session.delete(itor)

    db.session.commit()
    return restfulApi.make_response({'bResult': True, 'error': u' Done!'}, 200, headers='')


#删除对象接口
def deleteObject(UserId, ObjectId):
    delobj = Object.query.filter_by(OwnerUserId=UserId, Id=ObjectId).one()
    File.query.filter(File.Id.in_(
        db.session.query(Object.FileId.distinct()).filter(
            between(Object._Left_, delobj._Left_, delobj._Right_)).subquery())).update({
                                                                                           'RefCount': File.RefCount - db.session.query(
                                                                                               functions.count(
                                                                                                   Object.FileId)).filter(
                                                                                               between(Object._Left_,
                                                                                                       delobj._Left_,
                                                                                                       delobj._Right_),
                                                                                               Object.OwnerUserId == UserId).subquery()},
                                                                                       synchronize_session=False)
    (size,) = db.session.query(functions.sum(Object.Size)).filter(between(Object._Left_, delobj._Left_, delobj._Right_),
                                                                  Object.OwnerUserId == UserId).one()
    if size is None:
        size = 0
    u = User.query.filter(User.Id == UserId).one()
    u.Domain.UsedSize = u.Domain.UsedSize - size
    if u.Domain.UsedSize < 0:
        u.Domain.UsedSize = 0
    Object.query.filter(between(Object._Left_, delobj._Left_, delobj._Right_),
                        Object.OwnerUserId == UserId).delete(synchronize_session=False)
    n = (delobj._Right_ - delobj._Left_ ) / 2 + 1
    Object.query.filter(Object._Left_ >= delobj._Right_, Object.OwnerUserId == UserId).update(
        {'_Left_': Object._Left_ - 2 * n})
    Object.query.filter(Object._Right_ >= delobj._Right_, Object.OwnerUserId == UserId).update(
        {'_Right_': Object._Right_ - 2 * n})
    return n


@moudule.route('/delObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def delObject():  #TODO:容量计算不正确？
    session = request.session
    param = request.json_param

    del_ids = []
    if u'Ids' in param:
        del_ids = param[u'Ids']
    else:
        del_ids.append(param[u'Id'])
    for del_id in del_ids:
        UserId = objectOperatePermission(del_id, session['UserId'], 'storage', 'delete')

        zi = ZoneItem.query.filter_by(ObjectId=del_id).all()
        if len(zi) > 0:
            return {'failedContent': u'请先移除您个人主页中该资源对应的展示视频'}

        ap = AttachmentProtect.query.filter_by(ObjectId=del_id).all()
        for o in ap:
            if datetime.datetime.now() < o.Deadline:
                return {'failedContent': u'该资源处于锁定状态，因为它是需求成片，请在锁定日期失效后再尝试删除'}
        RequirementAttachment.query.filter_by(ObjectId=del_id).delete()
        CommentVideo.query.filter_by(ObjectId=del_id).delete()
        StorageShare.query.filter_by(ObjectId=del_id).delete()
        ContractAttachment.query.filter_by(ObjectId=del_id).delete()
        FollowerAttachment.query.filter_by(ObjectId=del_id).delete()
        deleteObject(UserId, del_id)
    db.session.commit()
    return {'affect_rows': len(del_ids)}


@moudule.route('/uploadFile/easy', methods=['GET', 'POST'])
@output_data
def upload_file_easy():
    param = request.json_param
    for f in request.files:
        f = request.files[f]
        if not (f and allowed_file(f.filename, IMAGE_TYPE)):
            raise APIException(SystemErrorCode.NonSupportFileType, u'禁止上传的文件类型', request.path)
        filename = str(uuid4())
        save_path = G_UPLOAD_FILE_FLODER
        visit_path = VISIT_FILE_FOLDER
        if param[u'useAge'] == 'zoneItemPortrait':
            save_path = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, 'temp')
            visit_path = os.path.join(VISIT_FILE_FOLDER, G_ZONE_PIC, 'temp')
        elif param[u'useAge'] == 'loginImage':
            save_path = os.path.join(G_UPLOAD_FILE_FLODER, 'loginImage')
            visit_path = os.path.join(VISIT_FILE_FOLDER, 'loginImage')
        elif param[u'useAge'] == 'activity':
            save_path = os.path.join(G_UPLOAD_FILE_FLODER, 'activityImage')
            visit_path = os.path.join(VISIT_FILE_FOLDER, 'activityImage')
        elif param[u'useAge'] == 'userPortrait':
            save_path = os.path.join(G_UPLOAD_FILE_FLODER, G_USER_PORTRAIT, 'temp')
            visit_path = os.path.join(VISIT_FILE_FOLDER, G_USER_PORTRAIT, 'temp')
        elif param[u'useAge'] == 'zoneBG':
            save_path = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, 'temp')
            visit_path = os.path.join(VISIT_FILE_FOLDER, G_ZONE_PIC, 'temp')
        elif param[u'useAge'] == 'zoneItem':
            save_path = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, 'temp')
            visit_path = os.path.join(VISIT_FILE_FOLDER, G_ZONE_PIC, 'temp')
        elif param[u'useAge'] == 'objectVideo':
            save_path = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, 'temp')
            visit_path = os.path.join(VISIT_FILE_FOLDER, G_ZONE_PIC, 'temp')

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_path = os.path.join(save_path, filename)
        f.save(save_path)

        if param[u'useAge'] == 'zoneItem' or param[u'useAge'] == 'objectVideo':
            im = Image.open(save_path)
            width = im.size[0]
            height = im.size[1]
            if width > height:
                bakSize = width
                left = 0
                right = width
                top = (width - height) / 2
                bottom = top + height
            else:
                bakSize = height
                top = 0
                bottom = height
                left = (height - width) / 2
                right = left + width
            bakImg = Image.new("RGBA", (bakSize, bakSize), (0, 0, 0))
            bakImg.save(save_path + '.bak', 'PNG')
            box = (left, top, right, bottom)
            region = im.crop((0, 0, width, height))
            bakImg.paste(region, box)
            os.remove(save_path)
            bakImg.save(save_path + '.png')
            os.remove(save_path + '.bak')
            return {'filePath': os.path.join(visit_path, filename + '.png'), 'fileName': filename + '.png'}
        return {'filePath': os.path.join(visit_path, filename), 'fileName': filename}


@moudule.route('/saveToMyStorage', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveToMyStorage():
    param = request.json_param
    session = request.session
    try:
        ca = ContractAttachment.query.filter_by(Id=param[u'attachmentId']).one()
        domain = Domain.query.filter_by(Id=session['DomainId']).one()
        owner = User.query.filter_by(Id=domain.OwnerUserId).one()
        root_obj = Object.query.filter_by(OwnerUserId=owner.Id, ParentId=None).one()
        if u'destObjId' in param:
            try:
                root_obj = Object.query.filter_by(OwnerUserId=owner.Id, Id=param[u'destObjId']).one()
            except NoResultFound:
                pass
        srcObj = Object.query.filter_by(Id=ca.ObjectId).one()
        destObj = Object(getSecurityObjectName(root_obj.Id, srcObj.Name, True), root_obj._Right_,
                              root_obj._Right_ + 1, root_obj.Id, owner.Id, owner.Id, srcObj.Size)
        Object.query.filter(Object._Left_ >= root_obj._Right_).update({'_Left_': Object._Left_ + 2})
        Object.query.filter(Object._Right_ >= root_obj._Right_).update({'_Right_': Object._Right_ + 2})
        srcObj.File.RefCount += 1
        destObj.FileId = srcObj.FileId
        destObj.Type = srcObj.Type
        db.session.add(destObj)
        db.session.commit()
        return {}
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'数据不存在')


def uploadFile_common(UserId):
    param = request.values
    share = ShareId = None
    if int(param[u'Id']) != 0:  #非附件
        uploaddirinfo = Object.query.filter_by(Id=param[u'Id']).one()
    else:  #附件
        root = Object.query.filter_by(OwnerUserId=UserId, ParentId=None).one()
        try:
            uploaddirinfo = root.Children.filter_by(Name=u'附件').one()
            share = uploaddirinfo.Shares[0]
            ShareId = share.Id
        except NoResultFound:
            uploaddirinfo = createDirObject(root.Id, UserId, u'附件')
            db.session.flush()
            share = Share('附件', UserId, uploaddirinfo.Id)
            shareuser = ShareUser(0, 1, 0, 0, 0, 0)  # 全局共享
            share.Users.append(shareuser)
            db.session.add(share)
            db.session.add(shareuser)
            RefreshShareCache(share)
            db.session.flush()

            ShareId = share.Id
    userinfo = User.query.filter_by(Id=UserId).one()
    surplus = userinfo.Domain.DefaultStorageSize + userinfo.Domain.ExtendStorageSize - userinfo.Domain.UsedSize
    saved_files = []
    objectsAdded = []
    try:
        if not UserId == uploaddirinfo.OwnerUserId:
            return APIException(SystemErrorCode.NonPermissionUpload, u'没有权限上传', request.path)
        for file in request.files:
            file = request.files[file]
            if not (file and allowed_file(file.filename)):
                raise APIException(SystemErrorCode.NonSupportFileType, u'禁止上传的文件类型', request.path)
            upload_filename = file.filename
            filename = str(uuid4())
            abspath = os.path.abspath(G_UPLOAD_FILE_FLODER)
            filepath = os.path.join(G_UPLOAD_FILE_FLODER, filename)
            file.save(filepath)
            saved_files.append(filepath)
            Size = os.path.getsize(filepath)
            MD5 = calMd5(filepath)
            if Size > surplus:
                raise APIException(DataErrorCode.NoStorageSize, u'一个或多个文件上传失败，存储空间不足', request.path)
            try:
                fileinfo = File.query.filter_by(MD5=MD5).one()
                os.remove(filepath)
                fileinfo.RefCount += 1
            except NoResultFound as e:
                fileinfo = File(getExtName(upload_filename), os.path.relpath(filepath, abspath), MD5, Size, 1)
                db.session.add(fileinfo)
            uploadObject = Object(getSecurityObjectName(uploaddirinfo.Id, upload_filename, True), uploaddirinfo._Right_,
                                  uploaddirinfo._Right_ + 1, uploaddirinfo.Id, UserId, UserId, Size)
            Object.query.filter(Object._Left_ >= uploaddirinfo._Right_).update({'_Left_': Object._Left_ + 2})
            Object.query.filter(Object._Right_ >= uploaddirinfo._Right_).update({'_Right_': Object._Right_ + 2})
            fileinfo.Objects.append(uploadObject)
            db.session.add(uploadObject)
            u = User.query.filter(User.Id == UserId).one()
            u.Domain.UsedSize = u.Domain.UsedSize + Size
            db.session.commit()
            uploadObject.Id
            obj = uploadObject.__dict__
            if ShareId is not None:
                obj[u'ShareId'] = ShareId
            objectsAdded.append(obj)
    except Exception as e:
        for file in saved_files:
            os.unlink(file)
        raise e
    return objectsAdded


def verify_uploadFile():
    param = request.json_param
    session = request.session
    UserId = session['UserId']
    if int(param[u'Id']) != 0:  #非附件
        uploaddirinfo = Object.query.filter_by(Id=param[u'Id']).one()
    else:  #附件
        root = Object.query.filter_by(OwnerUserId=UserId, ParentId=None).one()
        try:
            uploaddirinfo = root.Children.filter_by(Name=u'附件').one()
        except NoResultFound:
            uploaddirinfo = Object.query.filter_by(Id=root.Id).one()
    userinfo = User.query.filter_by(Id=UserId).one()
    surplus = userinfo.Domain.DefaultStorageSize + userinfo.Domain.ExtendStorageSize - userinfo.Domain.UsedSize

    if not UserId == uploaddirinfo.OwnerUserId:
        return 1
    if not (allowed_file(param[u'FileName'])):
        return 2
    if long(param[u'FileSize']) > surplus:
        return 3
    return 0


def smartUpload_save(UserId, fileInfo, filePath):
    print fileInfo
    param = request.values
    ShareId = None

    if int(param[u'Id']) != 0:  #非附件
        uploaddirinfo = Object.query.filter_by(Id=param[u'Id']).one()
    else:  #附件
        root = Object.query.filter_by(OwnerUserId=UserId, ParentId=None).one()
        try:
            uploaddirinfo = root.Children.filter_by(Name=u'附件').one()
            share = uploaddirinfo.Shares[0]
            ShareId = share.Id
        except NoResultFound:
            uploaddirinfo = createDirObject(root.Id, UserId, u'附件')
            db.session.flush()
            share = Share('附件', UserId, uploaddirinfo.Id)
            shareuser = ShareUser(0, 1, 0, 0, 0, 0)  # 全局共享
            share.Users.append(shareuser)
            db.session.add(share)
            db.session.add(shareuser)
            RefreshShareCache(share)
            db.session.flush()
            ShareId = share.Id
    objectsAdded = []
    abspath = os.path.abspath(G_UPLOAD_FILE_FLODER)
    try:
        MD5 ="adsewfewfe" #calMd5(filePath)
        try:
            fileObj = File.query.filter_by(MD5=MD5).one()
            fileObj.RefCount += 1
        except NoResultFound as e:
            fileObj = File(getExtName(fileInfo.FileName), os.path.relpath(filePath, abspath), MD5, fileInfo.TotalSize, 1)
            db.session.add(fileObj)
            if is_video(getExtName(fileInfo.FileName)):
                from Main import iconGenerator
                iconGenerator.addTask(filePath, "10", filePath + ".jpg")
            try:
                os.remove(filePath + "temp")
            except WindowsError:
                pass
        uploadObject = Object(getSecurityObjectName(uploaddirinfo.Id, fileInfo.FileName, True), uploaddirinfo._Right_,
                              uploaddirinfo._Right_ + 1, uploaddirinfo.Id, UserId, UserId, fileInfo.TotalSize)
        Object.query.filter(Object._Left_ >= uploaddirinfo._Right_).update({'_Left_': Object._Left_ + 2})
        Object.query.filter(Object._Right_ >= uploaddirinfo._Right_).update({'_Right_': Object._Right_ + 2})
        if is_video(getExtName(fileInfo.FileName)):
            uploadObject.Type = ObjectType.Video
        elif is_image(getExtName(fileInfo.FileName)):
            uploadObject.Type = ObjectType.Image
        elif is_document(getExtName(fileInfo.FileName)):
            uploadObject.Type = ObjectType.Document
        else:
            uploadObject.Type = ObjectType.Other

        fileObj.Objects.append(uploadObject)
        db.session.add(uploadObject)
        u = User.query.filter(User.Id == UserId).one()
        u.Domain.UsedSize = u.Domain.UsedSize + fileInfo.TotalSize
        db.session.commit()
        uploadObject.Id
        obj = uploadObject.__dict__
        obj[u'File'] = {"Path": fileObj.Path, "Ext": fileObj.Ext}
        if ShareId is not None:
            obj[u'ShareId'] = ShareId
        objectsAdded.append(obj)
    except Exception as e:
        raise e
    return objectsAdded


def is_video(suffix, video_type=VIDEO_TYPE):
    return suffix.lower() in video_type


def is_image(suffix, image_type=IMAGE_TYPE):
    return suffix.lower() in image_type


def is_document(suffix, document_type=DOCUMENT_TYPE):
    return suffix.lower() in document_type


@moudule.route('/bindingAccount', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def bindingAccount():
    session = request.session
    param = request.json_param
    UserId = session['UserId']
    user = User.query.filter_by(Id=UserId).one()
    user.Domain.Alipay = param[u'account']
    db.session.commit()
    return user


# 登陆后设置DBToken  来进行权限验证..
#上传后的文件存储数据库
#filecode参数
@moudule.route('/addFile', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def addvideofile():
    # 获取指定的参数
    # 权限认证过后 插入数据库
    session = request.session
    user_id = session['UserId']
    file_name = request.values["FileName"]
    file_size = request.values["FileSize"]
    file_thumb_path = request.values["FileThumbUrl"]
    file_transcode_path = request.values["FileTranscodedUrl"]
    file_identity = request.values["Filecode"]
    file_path = request.values["FilePath"]
    file_status = request.values["status"]
    file_md5 = request.values["md5"]
    dir_id = request.values["Id"]

    #判断文件的类型
    if is_video(getExtName(file_name)):
        file_type = ObjectType.Video
    elif is_image(getExtName(file_name)):
        file_type = ObjectType.Image
    elif is_document(getExtName(file_name)):
        file_type = ObjectType.Document
    else:
        file_type = ObjectType.Other

    # 查找上传文件所在的父目录
    try:
        dir_info = Object.query.filter_by(Id=dir_id).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'上传文件无父节点，异常情况')

    # 添加文件表项
    try:
        file_item = File.query.filter_by(MD5=file_md5).one()
        file_item.RefCount += 1
    except NoResultFound:
        # 文件videoUrl，视频文件为转码文件路径，其他文档为文件存储路径
        if file_type == ObjectType.Video:
            video_url = file_path
            # video_url = file_transcode_path
        else:
            video_url = file_path
        file_item = File(getExtName(file_name), file_thumb_path, file_md5, file_size, 1, video_url, file_identity)
        if file_type == ObjectType.Video:
            file_item.Status = file_status
        else:
            file_item.Status = 1
        db.session.add(file_item)
    print video_url

    # 添加object表项
    npos = file_name.rfind('.')
    if npos != -1:
        file_name_no_prefix = file_name[0:npos]
    obj_item = Object(getSecurityObjectName(dir_info.Id, file_name, True), dir_info._Right_,
                          dir_info._Right_ + 1, dir_info.Id, user_id, user_id, file_size)
    obj_item.Type = file_type
    Object.query.filter(Object._Left_ >= dir_info._Right_).update({'_Left_': Object._Left_ + 2})
    Object.query.filter(Object._Right_ >= dir_info._Right_).update({'_Right_': Object._Right_ + 2})
    file_item.Objects.append(obj_item)
    db.session.add(obj_item)

    # 更新用户空间信息
    u = User.query.filter(User.Id == user_id).one()
    u.Domain.UsedSize = u.Domain.UsedSize + int(file_size)
    db.session.commit()

    obj_item.Id
    obj = obj_item.__dict__
    obj[u'File'] = obj_item.File.__dict__
    result = []
    result.append(obj)

    return result


@moudule.route('/getDomainInfo', methods=['GET', 'POST'])
@output_data_without_attribute(['Password', 'MD5'])
@output_data
def getDomainInfo():
    param = request.json_param
    d = Domain.query.filter_by(Id=param[u'DomainId']).one()
    return d


# for流媒体服务器，通知应用服务器文件转码情况
@moudule.route('/transcodeStatus', methods=['GET', 'POST'])
@output_data
def transcodeStatus():
    param = request.json_param

    file_code = param[u'filecode']
    status = param[u'status']
    mp4file = param[u'mp4file']

    try:
        rs = File.query.filter_by(FileCode=file_code)
        rs.update({'Status': status, 'VideoFile': mp4file})
        db.session.commit()
    except Exception as e:
        return {"status": "failed", "Desc" : e.message}

    return {"status": "done"}


@moudule.route('/storageShareObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def storageShareObject():
    param = request.json_param
    session = request.session

    objectOperatePermission(param[u'ObjectId'], session['UserId'], 'storage', 'write')
    for d in param[u'DomainId']:
        try:
            StorageShare.query.filter_by(ObjectId=param[u'ObjectId'], DomainId=d).one()
            continue
        except NoResultFound:
            pass
        obj = Object.query.filter_by(Id=param[u'ObjectId']).one()
        user = User.query.filter_by(Id=obj.OwnerUserId).one()
        ss = StorageShare(param[u'ObjectId'], d, param[u'DownloadPermission'], param[u'WritePermission'], user.DomainId)
        db.session.add(ss)
    db.session.commit()
    return {}


@moudule.route('/getStorageShareObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getStorageShareObject():
    param = request.json_param
    ss = StorageShare.query.filter_by(ObjectId=param[u'ObjectId']).all()
    return ss


@moudule.route('/delStorageShareObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def delStorageShareObject():
    param = request.json_param
    StorageShare.query.filter_by(ObjectId=param[u'ObjectId']).delete()
    db.session.commit()
    return {}


@moudule.route('/delStorageShareObjectDomain', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def delStorageShareObjectDomain():
    param = request.json_param
    StorageShare.query.filter_by(ObjectId=param[u'ObjectId'], DomainId=param[u'DomainId']).delete()
    db.session.commit()
    ss = StorageShare.query.filter_by(ObjectId=param[u'ObjectId']).all()
    return ss


@moudule.route('/checkUserSize', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def checkUserSize():
    param = request.json_param
    session = request.session
    try:
        domain = Domain.query.filter_by(Id=session['DomainId']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'未找到该用户')
    left = domain.DefaultStorageSize + domain.ExtendStorageSize - domain.UsedSize - param[u'fileSize']
    if left < 0:
        return {'full': True}
    return {'full': False}



@moudule.route('/shareVideo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def shareVideo():
    param = request.json_param
    try:
        o = Object.query.filter_by(Id=param[u'ObjectId']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'未找到该资源')
    o.BShare = param[u'BShare']
    db.session.commit()
    return {}