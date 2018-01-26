# -*- coding: utf-8 -*-
from sqlalchemy import delete, or_, and_, outerjoin
from sqlalchemy.orm import contains_eager, joinedload, join

__author__ = 'admin'

from flask.module import Module
from Tools.SqliteSession import ManualSession
from Models.Database import db
from json import JSONDecoder
from Tools.DataPaser import output_data, output_data_without_attribute, expandAttribute
from Tools.Permision import PermissionValidate, GetSessionId, sharedPermissionValidate, Permission
from Tools.APIException import *
from flask.ext import restful
from flask import request
from Models.CloudStorge import *
from Models.Platform import *
from Models.Index import *
from sqlalchemy.orm.exc import NoResultFound
from Tools.GlobalVars import *
from shutil import copy
import os
import Image
moudule = Module(__name__)


def route_config(app, api):
    app.register_module(moudule, url_prefix='/share')


# 获取用户域信息
@moudule.route('/getDomainInfo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getDomainInfo():
    session = request.session
    # param = request.json_param
    UserId = session["UserId"]
    domain = User.query.filter_by(Id=UserId).one().Domain
    if domain.Status == DomainStatus.init:
        return APIException(SystemErrorCode.UnkonwnError, u'企业还未开通')
    result = domain.__dict__
    users = domain.Users.all()
    result['Roles'] = domain.Roles.all()
    result['Users'] = []
    for user in users:
        user = expandAttribute(user, ['Roles'])
        result['Users'].append(user)
    for u in result['Users']:
        del u['Domain']
    return result


# 创建域
@moudule.route('/createDomain', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def createDomain():
    param = request.json_param
    session = request.session
    UserId = session["UserId"]
    try:
        user = User.query.filter_by(Id=UserId).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无该用户信息')
        #公司注册

    if u'RealName' in param:
        user.RealName = param[u'RealName']
    if u'CellPhone' in param:
        user.Domain.CompanyCelPhone = param[u'CellPhone']

    user.Domain.DomainName = param[u'DomainName']
    user.Domain.Status = DomainStatus.use
    db.session.commit()
    return user


def addUserRole(role, param):
    (user, domain) = param
    user.DomainPermissionInvalidate = 1
    userrole = domain.Roles.filter_by(Id=role[u'Id']).one()
    if userrole not in user.Roles:
        user.Roles.append(userrole)


def delUserRole(role, param):
    (user, domain) = param
    user.DomainPermissionInvalidate = 1
    dbrole = domain.Roles.filter_by(Id=role[u'Id']).one()
    if dbrole.DomainAdmin == 1 and domain.OwnerUserId == user.Id:
        raise APIException(SystemErrorCode.UnkonwnError, u'域创建者必须是域管理员，不能删除')
    user.Roles.remove(dbrole)


def addDomainUser(user, domain):
    try:
        dbuser = User.query.filter_by(Id=user[u'Id']).one()
    except KeyError as e:
        dbuser = User(None, None, None)
        dbuser.CreateTime = datetime.datetime.now()
        dbuser.NickName = user[u'DomainName']
        dbuser.Password = user[u'Password']
    if dbuser.DomainId is not None:
        raise APIException(SystemErrorCode.UnkonwnError,u'不能将已加入其它企业的用户加入')
    domain.Users.append(dbuser)
    if domain.Users.filter_by(DomainName=user[u'DomainName']).count()>0:
        raise APIException(SystemErrorCode.UnkonwnError,u'企业中已存在（%s）'% user[u'DomainName'])
    dbuser.DomainName = user[u'DomainName']
    db.session.flush()
    process_list(user['Roles'], 'UserRole', (dbuser, domain))


def modifyDomainUser(user, domain):
    dbuser = domain.Users.filter_by(Id=user[u'Id']).one()

    if u'DomainName' in user:
        if domain.Users.filter(User.Id!=user[u'Id'], User.DomainName==user[u'DomainName']).count() > 0:
            raise APIException(SystemErrorCode.UnkonwnError, u'DomainName已存在（%s）' % user[u'DomainName'])
        dbuser.DomainName = user[u'DomainName']
    if u'Password' in user:
        dbuser.Password = user[u'Password']
    db.session.flush()
    process_list(user['Roles'], 'UserRole', (dbuser, domain))


def delDomainUser(user, domain):
    if domain.OwnerUserId == user[u'Id']:
        raise APIException(SystemErrorCode.UnkonwnError, u'域创建者必须是域成员，不能删除')
    UserRole.query.filter_by(UserId=user[u'Id']).delete()
    u = User.query.filter_by(Id=user[u'Id']).one()
    domain.Users.remove(u)
    db.session.delete(u)


def addDomainRole(role, domain):
    if domain.Roles.filter_by(Name=role[u'Name']).count() > 0:
        return APIException(DataErrorCode.DomainRoleExist, u'角色名已被占用')
    dbrole = Role(role[u'Name'], None, domain.OwnerUserId, 0)
    domain.Roles.append(dbrole)


def modifyDomainRole(role, domain):
    db.session.query(User).filter(UserRole.RoleId == role[u'Id']).update({User.DomainPermissionInvalidate: 1})
    dbrole = domain.Roles.filter_by(Id=role[u'Id']).one()
    if dbrole.DomainAdmin == 1:
        return APIException(SystemErrorCode.UnkonwnError, u'超级管理员角色不允许修改！')
    if u'Name' in role:
        dbrole.Name = role[u'Name']


def delDomainRole(role, domain):
        # user = db.session.query(User).filter(UserRole.RoleId == role[u'Id']).one()
        # user.DomainPermissionInvalidate = 1
    UserRole.query.filter_by(RoleId=role[u'Id']).delete()
    domain.Roles.filter_by(Id=role[u'Id']).delete()
    RoleRight.query.filter_by(RoleId=role[u'Id']).delete()


def OperateKey(item):  # 操作优先级 修改>删除>添加
    oper = item[u'Operate'].lower()
    if oper == 'add':
        return 3
    elif oper == 'del':
        return 2
    elif oper == 'modify':
        return 1
    return 0


def process_list(list, suffix, param=None):
    sorted(list, key=OperateKey)  # 按操作优先级排序，以免数据先加加不上后删除导致数据与预期不一致
    for item in list:
        try:
            func = globals()[item[u'Operate'] + suffix]
        except KeyError:  # 函数不存在时，KeyError
            print u"无效操作接口：" + item[u'Operate'] + suffix
            raise APIException(SystemErrorCode.UnkonwnError, u"无效操作接口")
        func(item, param)


# 修改域信息
@moudule.route('/modifyDomainInfo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def modifyDomainInfo():
    session = request.session
    param = request.json_param
    UserId = session["UserId"]
    domaininfo = Domain.query.filter_by(Id=param[u'Id']).one()
    if u'DomainName' in param:
        if Domain.query.filter_by(DomainName=param[u'DomainName']).count() > 0:
            return APIException(DataErrorCode.DomainNameExist, u'域名已被占用')
        domaininfo.DomainName = param[u'DomainName']
    if u'Roles' in param:
        process_list(param[u'Roles'], 'DomainRole', domaininfo)
    if u'Users' in param:
        process_list(param[u'Users'], 'DomainUser', domaininfo)
    db.session.commit()
    domaininfo.Id
    result = domaininfo.__dict__
    result['Roles'] = domaininfo.Roles.all()
    users = domaininfo.Users.all()
    result['Users'] = []
    for user in users:
        result['Users'].append(user.__dict__)
    for u in result['Users']:
        del u['Domain']
    return result


# 查找用户
@moudule.route('/searchDomain', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['Password'])
@output_data
def searchDomain():
    param = request.json_param
    searchPhase = "%" + param[u'KeyWord'] + "%"
    domains = Domain.query.filter(or_(Domain.CompanyName.like(searchPhase))).all()
    return domains
    # users = db.session.query(User, Domain).outerjoin(Domain, User.DomainId == Domain.Id)\
    #     .filter(or_(User.DomainName == param[u'KeyWord'], User.Email == param[u'KeyWord'])).all()
    # us = []
    # for u in users:
    #     uu = u[0]
    #     uu.Domain = u[1]
    #     us.append(uu)
    # return us


#删除域
@moudule.route('/delDomain', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def delDomain():
    session = request.session
    param = request.json_param
    UserId = session["UserId"]
    if (db.session.query(Domain.OwnerUserId).filter_by(Id=param['Id']).one()) == (UserId,):
        res = Domain.query.filter_by(Id=param['Id']).delete()
    else:
        return APIException(SystemErrorCode.NonPermissionDelete, u'没有权限删除')
    return {"res": res}


#共享对象
def RefreshShareCache(shareobject):
    shareobject.UsersCache.delete() #清空缓存
    users = {}
    for u in shareobject.Users:
        user = ShareUserCache(u.UserId, u.UserRead, u.UserWrite, u.UserCreate, u.UserDelete, u.UserDownload)
        shareobject.UsersCache.append(user)
        users[u.UserId] = {'u': user, 'o': True}
    for g in shareobject.Groups:
        for u in g.Users:
            if u.Id not in users:
                user = ShareUserCache(u.Id, g.GroupRead, g.GroupWrite, g.GroupCreate, g.GroupDelete, g.GroupDownload)
                shareobject.UsersCache.append(user)
                users[u.Id] = {'u': user, 'o': False}
            else:
                if users[u.Id]['o'] == False:
                    user = users[u.Id]['u']
                    if user.UserRead == 0:
                        user.UserRead = g.GroupRead
                    if user.UserWrite == 0:
                        user.UserWrite = g.GroupWrite
                    if user.UserCreate == 0:
                        user.UserCreate = g.GroupCreate
                    if user.UserDelete == 0:
                        user.UserDelete = g.GroupDelete
                    if user.UserDownload == 0:
                        user.UserDownload = g.GroupDownload
    db.session.flush()
    for u in users.keys():
        db.session.add(users[u]['u'])

def shareAttachment(param):
    objectUserId = sharedPermissionValidate(Permission.PermissionShare, param=param)
    obj = Object.query.filter_by(OwnerUserId=objectUserId, Id=param[u'Id']).one()
    UserId = request.session['UserId']
    try:
        shareobject = Share.query.filter_by(CreatorUserId=UserId, ObjectId=param[u"Id"]).one()
    except NoResultFound:
        shareobject = Share(obj.Name, UserId, param[u'Id'])  #添加共享对象
        db.session.add(shareobject)
    if u'Groups' in param:
        for g in param[u'Groups']:
            try:
                group=shareobject.Groups.filter_by(GroupName=g[u'GroupName']).one()
                g[u'Operate'] =u'modify'
                g[u'Id']=group.Id
            except NoResultFound:
                g[u'Operate'] =u'add'
        process_list(param[u'Groups'], 'ShareGroup', shareobject)
    if u'Users' in param:
        process_list(param[u'Users'], 'ShareUser', shareobject)
    db.session.flush()
    RefreshShareCache(shareobject)
    db.session.flush()
    return shareobject.Id


@moudule.route('/shareObject', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def shareObject():
    session = request.session
    param = request.json_param
    objectUserId = sharedPermissionValidate(Permission.PermissionShare)
    UserId = session["UserId"]
    if u'DomainId' in param and ( u'Groups' in param or u'Users' in param):  # objectUserId!=UserId:  # 域内容共享
        permissions = [Permission.PermissionWrite, Permission.PermissionCreate,
                       Permission.PermissionDelete, Permission.PermissionDownload]
        for i in range(len(permissions)-1, -1, -1):
            if session['domainPermission' + permissions[i].name[10:]] == 1:
                permissions.remove(permissions[i])
        if u'Groups' in param:
            for g in param[u'Groups']:
                for p in permissions:
                    if g[u'Group' + p.name[10:]] == 1:
                        raise APIException(SystemErrorCode.UnkonwnError, u'不能将自己不具备的权限在共享时赋给他人')
        if u'Users' in param:
            for u in param[u'Users']:
                for p in permissions:
                    if u[u'User' + p.name[10:]] == 1:
                        raise APIException(SystemErrorCode.UnkonwnError, u'不能将自己不具备的权限在共享时赋给他人')
    Name = None
    #权限验证
    Object.query.filter_by(OwnerUserId=objectUserId, Id=param[u'Id']).one()
    if u'Name' in param:
        Name = param[u'Name']
    try:
        shareobject = Share.query.filter_by(CreatorUserId=UserId, ObjectId=param[u"Id"]).one()
        if len(param) != 2:#只有两个参数时是取信息
            ShareUserCache.query.filter_by(ShareObjectId=shareobject.Id).delete()
    except NoResultFound:
        if Name is None:
            return
        shareobject = Share(Name, UserId, param[u'Id'])  #添加共享对象
        db.session.add(shareobject)

    if Name is not None:
        shareobject.Name = Name
    if u'Groups' in param:
        process_list(param[u'Groups'], 'ShareGroup', shareobject)
    if u'Users' in param:
        process_list(param[u'Users'], 'ShareUser', shareobject)
    db.session.flush()
    if len(param)!=2:  # 只有两个参数时是取信息
        RefreshShareCache(shareobject)

    db.session.commit()
    shareobject.Id
    result = shareobject.__dict__

    result['Groups'] = db.session.query(Group).options(joinedload(Group.Users, innerjoin=False)).filter(
        Group.ShareObjectId == shareobject.Id).all()
    result['Users'] = shareobject.Users.all()
    return result


#取消共享
@moudule.route('/cancelShare', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def cancelShare():
    session = request.session
    param = request.json_param
    UserId = session["UserId"]
    canncelobject = Share.query.filter_by(ObjectId=param[u'ObjectId'], CreatorUserId=UserId).one()
    ShareUser.query.filter_by(ShareObjectId=canncelobject.Id).delete()
    ShareUserCache.query.filter_by(ShareObjectId=canncelobject.Id).delete()
    # SQLAlchemy cannot do delete with join, so the hard code here
    db.session.execute(
        "DELETE groupuser FROM groupuser INNER JOIN `group` ON `group`.`Id` = groupuser.`GroupId` WHERE `group`.`ShareObjectId` = :ShareObjectId;",
        {'ShareObjectId': canncelobject.Id})
    Group.query.filter_by(ShareObjectId=canncelobject.Id).delete()
    db.session.delete(canncelobject)
    db.session.commit()
    return canncelobject


def addGroupUser(groupuser, group):
    if group.UsersQuery.filter_by(Id=groupuser[u'Id']).count() > 0:  # 避免重复加入
        return
    group.UsersQuery.append(User.query.filter_by(Id=groupuser[u'Id']).one())


def delGroupUser(groupuser, group):
    group.Users.remove(User.query.filter_by(Id=groupuser[u'Id']).one())


def addShareGroup(group, share):
    dbgroup = Group(group[u'GroupName'], group[u'GroupRead'], group[u'GroupWrite'], group[u'GroupCreate'],
                    group[u'GroupDelete'],group[u'GroupDownload'])
    db.session.add(dbgroup)
    share.Groups.append(dbgroup)
    if u'Users' in group:
        process_list(group[u'Users'], 'GroupUser', dbgroup)


def modifyShareGroup(group, share):
    dbgroup = Group.query.filter_by(Id=group[u'Id']).one()
    dbgroup.GroupName = group[u'GroupName']
    dbgroup.GroupRead = group[u'GroupRead']
    dbgroup.GroupWrite = group[u'GroupWrite']
    dbgroup.GroupCreate = group[u'GroupCreate']
    dbgroup.GroupDelete = group[u'GroupDelete']
    dbgroup.GroupDownload = group[u'GroupDownload']
    if u'Users' in group:
        process_list(group[u'Users'], 'GroupUser', dbgroup)


def delShareGroup(group, share):
    GroupUser.query.filter_by(GroupId=group[u'Id']).delete()
    Group.query.filter_by(Id=group[u'Id']).delete()


def addShareUser(shareuser, share):
    userid = shareuser[u'UserId']
    # 不是新共享的对象
    if share.Id is not None:
        if share.Users.filter_by(UserId=userid).count() > 0:  # 避免重复加入
            return
    dbshareuser = ShareUser(userid, shareuser[u'UserRead'], shareuser[u'UserWrite'],
                            shareuser[u'UserCreate'], shareuser[u'UserDelete'],shareuser[u'UserDownload'])
    share.Users.append(dbshareuser)
    db.session.add(dbshareuser)


def modifyShareUser(shareuser, share):
    dbshareuser = share.Users.filter_by(Id=shareuser[u'Id']).one()
    dbshareuser.UserRead = shareuser[u'UserRead']
    dbshareuser.UserWrite = shareuser[u'UserWrite']
    dbshareuser.UserCreate = shareuser[u'UserCreate']
    dbshareuser.UserDelete = shareuser[u'UserDelete']
    dbshareuser.UserDownload = shareuser[u'UserDownload']

def delShareUser(shareuser, share):
    share.Users.filter_by(Id=shareuser[u'Id']).delete()


@moudule.route('/getShareUsers', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def modifyShareObject():
    session = request.session
    param = request.json_param
    UserId = session["UserId"]
    shareobjectinfo = Domain.query.filter_by(Id=param[u'Id']).one()
    if u'Name' in param:
        shareobjectinfo.Name = param[u'Name']
    if u'Groups' in param:
        process_list(param[u'Groups'], 'DomainRole', shareobjectinfo)
    if u'UserInfos' in param:
        process_list(param[u'UserInfos'], 'DomainUser', shareobjectinfo)
    db.session.commit()
    shareobjectinfo.Id
    result = shareobjectinfo.__dict__
    result['Groups'] = shareobjectinfo.Groups.all()
    result['Users'] = shareobjectinfo.Users.all()
    return result
    UserId = session['UserId']
    shareUsers = db.session.query(Share.CreatorUserId.distinct()).filter(ShareUser.UserId == UserId).all()
    ShareUser.query.filter_by(UserId=UserId).all()

@moudule.route('/addZoneBg', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def addzonebg():
    param = request.json_param
    domain = db.session.query(Domain).filter(Domain.Id == param[u'DomainId']).one()
    left = param[u'left']
    top = param[u'top']
    right = param[u'right']
    bottom = param[u'bottom']
    bCut = False
    if right - left > 0 and bottom - top > 0:
        bCut = True
    cur_time = datetime.datetime.now().strftime('%y-%m')
    portrait = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, 'temp', param[u'file'])
    destDir = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, cur_time)
    savePath = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, cur_time, param[u'file'] + '.png')
    destPortrait = os.path.join(VISIT_FILE_FOLDER, G_ZONE_PIC, cur_time, param[u'file'] + '.png')
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
            copy(portrait, destDir)
        os.remove(portrait)
        if domain.ZoneBanner:
            delPortrait = G_STATIC_FOLDER + domain.ZoneBanner
            if os.path.exists(delPortrait):
                os.remove(delPortrait)
        domain.ZoneBanner = destPortrait
        db.session.commit()
    return

@moudule.route('/addWall', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def addwall():
    param = request.json_param
    for value in param[u'files']:
        item = ZoneItem(param[u'DomainId'], value[u'Id'], datetime.datetime.now())
        item.Type = ZoneItemType.Picture
        item.Price = 0
        item.Weight = 0
        item.Classical = 0
        db.session.add(item)
    db.session.commit()
    item.Object.File.Path
    return item

@moudule.route('/modifyPicIntro', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def modifypicintro():
    param = request.json_param
    zi = db.session.query(ZoneItem).filter(ZoneItem.Id == param[u'id']).one()
    zi.Intro = param[u'text']
    db.session.commit()
    return

@moudule.route('/editVideoToZone', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def EditVideoToZone():
    param = request.json_param
    session = request.session
    user = User.query.filter_by(Id=session['UserId']).one()
    item = db.session.query(ZoneItem).filter(ZoneItem.Id == param[u'FileId']).one()
    item.Intro = param[u'Intro']
    item.Weight = 0
    item.Price = float(param[u'Price'])
    if item.Price < 0:
        item.Price = 0
    item.ReferPrice = float(param[u'ReferPrice'])
    item.BasePrice = float(param[u'bp'])
    item.SchemePrice = float(param[u'scp'])
    item.ShotPrice = float(param[u'shp'])
    item.ActorPrice = float(param[u'acp'])
    item.MusicPrice = float(param[u'mp'])
    item.AEPrice = float(param[u'aep'])
    if user.Domain.Count > float(param[u'Price']):
        item.Weight = 1
    item.Classical = 0
    object = Object.query.filter_by(Id=item.ObjectId).one()
    object.Category_1 = param[u'Category_1']
    object.Category_2 = param[u'Category_2']
    object.Tag = Category.query.filter_by(Id=param[u'Category_1']).one().Name+' '+\
                 Category.query.filter_by(Id=param[u'Category_2']).one().Name
    for index in range(len(param[u'TagsArray'])):
         try:
             Tag.query.filter_by(Name=param[u'TagsArray'][index]).one()
         except NoResultFound:
             if param[u'TagsArray'][index]!='':
                 tag = Tag()
                 tag.Name = param[u'TagsArray'][index]
                 tag.UserId = user.Id
                 db.session.add(tag)
                 db.session.commit()
         if index>1:
             object.Tag += ' '+param[u'TagsArray'][index]
    db.session.add(item)
    db.session.commit()
    return {'result': True}

@moudule.route('/addVideoToZone', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def AddVideoToZone():
    param = request.json_param
    session = request.session
    cur_time = datetime.datetime.now().strftime('%y-%m')
    try:
        portrait = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, 'temp', param[u'Portrait'])
    except:
        return {'result': False, 'info': '请添加视频图标'}
    destDir = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, cur_time)
    savePath = os.path.join(G_UPLOAD_FILE_FLODER, G_ZONE_PIC, cur_time, param[u'Portrait'] + '.png')
    destPortrait = os.path.join(VISIT_FILE_FOLDER, G_ZONE_PIC, cur_time, param[u'Portrait'] + '.png')
    bHasPortrait = False

    if param[u'Portrait']:
        left = param[u'left']
        top = param[u'top']
        right = param[u'right']
        bottom = param[u'bottom']
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
    try:
        db.session.query(ZoneItem).filter(and_(ZoneItem.DomainId == param[u'DomainId'],
                                          ZoneItem.ObjectId == param[u'FileId'])).one()
        return {'result': False, 'info': '该视频已添加，请勿重复添加'}
    except NoResultFound:
        if Object.query.filter_by(Id=param[u'FileId']).one().Type != 0:
            return {'result': False, 'info': '请确认添加的文件为视频格式'}
        user = User.query.filter_by(Id=session['UserId']).one()
        item = ZoneItem(param[u'DomainId'], param[u'FileId'], param[u'Intro'])
        item.Type = ZoneItemType.Video
        item.Weight = 0
        item.Price = float(param[u'Price'])
        if item.Price < 0:
            item.Price = 0
        item.ReferPrice = float(param[u'ReferPrice'])
        item.BasePrice = float(param[u'bp'])
        item.SchemePrice = float(param[u'scp'])
        item.ShotPrice = float(param[u'shp'])
        item.ActorPrice = float(param[u'acp'])
        item.MusicPrice = float(param[u'mp'])
        item.AEPrice = float(param[u'aep'])
        if user.Domain.Count > float(param[u'Price']):
            item.Weight = 1
        item.Classical = 0
        object = Object.query.filter_by(Id=param[u'FileId']).one()
        object.Category_1 = param[u'Category_1']
        object.Category_2 = param[u'Category_2']
        object.Tag = param[u'Tags']
        if bHasPortrait:
            item.Portrait = destPortrait
        else:
            item.Portrait = object.File.Path
        for val in param[u'TagsArray']:
             try:
                 Tag.query.filter_by(Name=val).one()
             except NoResultFound:
                 if val!='':
                     tag = Tag()
                     tag.Name = val
                     tag.UserId = user.Id
                     db.session.add(tag)
                     db.session.commit()
        object.Tag=Category.query.filter_by(Id=param[u'Category_1']).one().Name+' '+\
                   Category.query.filter_by(Id=param[u'Category_2']).one().Name+' '+param[u'Tags']
        db.session.add(item)
        db.session.commit()
        return {'result': True}

@moudule.route('/deleteVideoFromZone', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def DeleteVideoFromZone():
    param = request.json_param
    zi = db.session.query(ZoneItem).filter(ZoneItem.Id == param[u'Id']).one()
    destPortrait = G_STATIC_FOLDER + zi.Portrait
    if os.path.exists(destPortrait):
        os.remove(destPortrait)
    CollectionVideo.query.filter_by(ZoneItemId=zi.Id).delete()
    ZoneItem.query.filter_by(Id=param[u'Id']).delete()
    ClassicalSetting.query.filter_by(ZoneItemId=param[u'Id']).delete()
    db.session.commit()
    return

@moudule.route('/applyClassical', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def ApplyClassical():
    param = request.json_param
    zone_item = ZoneItem.query.filter_by(Id=param[u'Id']).one()
    zone_item.Classical = 1
    db.session.commit()
    return

@moudule.route('/saveIntroInZone', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def SaveIntroInZone():
    param = request.json_param
    session = request.session
    user = User.query.filter_by(Id=session['UserId']).one()
    user.Domain.Intro = param[u'text']
    db.session.commit()
    return


@moudule.route('/getWall', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute(['MD5'])
@output_data
def getwall():
    session = request.session
    user = db.session.query(User).filter(User.Id == session['UserId']).one()
    data = {}
    data['category'] = Category.query.all()
    data['tag_personal'] = Tag.query.filter_by(UserId=session['UserId']).all()
    data['tag_normal'] = Tag.query.filter_by(UserId=None).all()
    data['zone_item'] = ZoneItem.query.filter(and_(ZoneItem.DomainId==user.DomainId, ZoneItem.Type==ZoneItemType.Video)).all()
    data['zone_pic'] = ZoneItem.query.filter(and_(ZoneItem.DomainId==user.DomainId, ZoneItem.Type==ZoneItemType.Picture)).all()
    data['user'] = user
    data['zone_banner'] = user.Domain.ZoneBanner
    items = ZoneItem.query.order_by(ZoneItem.Price.desc()).limit(10).all()
    if len(items) > 0:
        data['priceRange'] = items[len(items) - 1].Price
    else:
        data['priceRange'] = 0
    return data

@moudule.route('/dropWall', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def dropwall():
    param = request.json_param
    session = request.session
    Id = param[u'id']
    ZoneItem.query.filter_by(Id=Id).delete()
    db.session.commit()
    zpic = ZoneItem.query.filter(and_(ZoneItem.DomainId == session['DomainId'], ZoneItem.Type == ZoneItemType.Picture)).all()
    return zpic


@moudule.route('/getUserSize', methods=['GET', 'POST'])
@output_data_without_attribute(['MD5'])
@PermissionValidate()
@output_data
def getusersize():
    session = request.session
    user = User.query.filter_by(Id=session['UserId']).one()
    am = ApplyMoney.query.filter_by(UserId=user.Id).all()
    user = expandAttribute(user, [])
    user['ApplyMoney'] = am
    return user


@moudule.route('/userRights', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def userRights():
    param = request.json_param
    rights = Right.query.all()
    if u'RoleId' in param:
        roleRights = RoleRight.query.filter_by(RoleId=param[u'RoleId']).all()
    else:
        roleRights = {}
    return {"rights": rights, "roleRights": roleRights}


@moudule.route('/saveRole', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveRole():
    param = request.json_param
    rights = Right.query.all()
    ur = param[u'Rights']
    if param[u'bNew']:
        role = Role(param[u'RoleName'], param[u'DomainId'], param[u'CreatorId'], 0)
        db.session.add(role)
        db.session.flush()
        for right in rights:
            if right.Leaf:
                sid = str(right.Id)
                roleRight = RoleRight(right.Id, role.Id, ur[sid])
                db.session.add(roleRight)
        db.session.commit()
        return role
    else:
        try:
            role = Role.query.filter_by(Id=param[u'RoleId']).one()
        except NoResultFound:
            return APIException(SystemErrorCode.UnkonwnError, u'无角色信息')
        role.Name = param[u'RoleName']
        try:
            roleRights = RoleRight.query.filter_by(RoleId=param[u'RoleId']).all()
            for roleRight in roleRights:
                sid = str(roleRight.RightId)
                roleRight.Checked = ur[sid]
        except NoResultFound:
            pass
    db.session.commit()
    return {}