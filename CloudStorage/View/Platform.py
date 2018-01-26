# -*- coding: utf-8 -*-
import base64
from datetime import datetime, timedelta
from json import JSONEncoder
from uuid import uuid4
import os
from dateutil import tz
import dateutil.parser
from flask import Module, request, g
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from Models.CloudStorge import Object, Share, User, PlatformSetting, Domain
from Models.Database import db
from Models.Index import *
from Models.Platform import *
    # Requirement, RequirementStatus, RequirementReply, RequirementReplyStatus, \
    # RequirementAttachment, Contract, ContractStatus, ContractReply, ContractSegment, ContractSegmentStatus, \
    # ContractSegmentType, Project, ProjectSegment, ProjectSegmentStatus, ContractUserGroup, ContractAttachment, \
    # ContractEventLog, ProjectEventLog, ContractHistory, Scheme, Script, \
    # ContractClips, ReviewVideo, FinalVideo, Order, ContractOrder, ContractOrderType, OrderState, ResourceShare, \
    # RequirementReplyGroup, MarkPoint, ContractSegmentLog, RequirementFollower, ContractLogActionType, \
    # Category, RequirementTemplate, ExtendStorageOrder, RechargeAccountOrder, MemberShipTaxOrder, \
    # ContractAttachmentType, OrderLog, PlatformMsg, ZoneItem, ContractAbortRecord, RequirementSegment
from Tools.APIException import APIException, SystemErrorCode, DataErrorCode
from Tools.DataPaser import output_data, output_data_without_attribute, expandAttribute, round_
from Tools.GlobalVars import G_UPLOAD_FILE_FLODER_REL
from Tools.Permision import PermissionValidate, sharedPermissionValidate, Permission, objectOperatePermission
from View.CloudStorgeView import deleteObject
from View.DomainView import shareAttachment
from Tools.AlipayDirectHelper import create_direct_pay_by_user

moudule = Module(__name__)


def route_config(app, api):
    app.register_module(moudule, url_prefix='/platform')


@moudule.route('/deleteRequirement', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def deleteRequirement():
    param = request.json_param
    try:
        requirement = Requirement.query.filter_by(Id=param[u'Id']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'需求不存在')

    if requirement.Status == RequirementStatus.Published or requirement.Status == RequirementStatus.Created:
        RequirementAttachment.query.filter_by(RequirementId=requirement.Id).delete()
        RequirementReplyGroup.query.filter_by(RequirementId=requirement.Id).delete()
        RequirementReply.query.filter_by(RequirementId=requirement.Id).delete()
        RequirementFollower.query.filter_by(RequirementId=requirement.Id).delete()
        RequirementSegment.query.filter_by(RequirementId=requirement.Id).delete()
        ResourceShare.query.filter_by(ResourceId=requirement.Id, ResourceType='r').delete()
        Contract.query.filter_by(RequirementId=requirement.Id).delete()
        db.session.delete(requirement)
        db.session.commit()
        return {}
    else:
        return APIException(SystemErrorCode.UnkonwnError, u'合同已经建立，无法删除需求')


@moudule.route('/publishRequirement', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def publishRequirement():
    session = request.session
    param = request.json_param

    bNew = True

    if u'Id' in param:
        try:
            requirement = Requirement.query.filter_by(Id=param[u'Id']).one()
        except NoResultFound:
            raise APIException(SystemErrorCode.UnkonwnError, u'需求不存在')

        bNew = False
    elif u'bCancel' not in param:
        requirement = Requirement()
        requirement.Status = RequirementStatus.Created
        requirement.PublisherId = session['UserId']
        db.session.add(requirement)

        rs = RequirementSegment(requirement.Id, RequirementStatus.Published)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.Contracting)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.PayDeposit)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.Reviewing)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.PayAll)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.Retainage)
        db.session.add(rs)

    # 取消提交
    if u'bCancel' in param:
        if requirement.Status == RequirementStatus.Published:
            requirement.Status = RequirementStatus.Created
            RequirementFollower.query.filter_by(RequirementId=requirement.Id).delete()
            db.session.commit()
        return requirement

    if u'Status' in param and param[u'Status'] != 0 and requirement.Status == RequirementStatus.Created:
        requirement.Status = RequirementStatus.Published
    if u'Deadline' in param:
        requirement.Deadline = param[u'Deadline']
    if u'long' in param:
        requirement.Long = param[u'long']
    if u'format' in param:
        requirement.Format = param[u'format']
    if u'voice' in param:
        requirement.Voice = param[u'voice']
    if u'subtitle' in param:
        requirement.Subtitle = param[u'subtitle']
    if u'gbm' in param:
        requirement.Gbm = param[u'gbm']
    if u'place' in param:
        requirement.Place = param[u'place']
    if u'refer' in param:
        requirement.Refer = param[u'refer']
    if u'symbol' in param:
        requirement.Symbol = param[u'symbol']
    if u'category_1' in param:
        requirement.Category_1 = param[u'category_1']
    if u'category_2' in param:
        requirement.Category_2 = param[u'category_2']
    if u'Detail' in param:
        requirement.Detail = param[u'Detail']
    if u'Amount' in param:
        requirement.Amount = round_(float(param[u'Amount']))
    if u'Title' in param:
        requirement.Title = param[u'Title']
    if u'Attachments' in param:
        for attachment in param[u'Attachments']:
            try:
                attach = RequirementAttachment.query\
                    .filter_by(RequirementId=requirement.Id, ObjectId=attachment[u'Id']).one()
                attach.Description = attachment[u'Description']
            except NoResultFound:
                ra = RequirementAttachment()
                ra.ObjectId = attachment[u'Id']
                ra.OperateUserId = session['UserId']
                ra.Description = attachment[u'Description']
                requirement.RequirementAttachment.append(ra)

    if bNew:
        db.session.flush()

    if u'specifyProducers' in param:
        ResourceShare.query.filter_by(ResourceId=requirement.Id, ResourceType='r').delete()
        if len(param[u'specifyProducers']) > 0:
            for domainId in param[u'specifyProducers']:
                r = ResourceShare(requirement.Id, 'r', domainId)
                db.session.add(r)
        else:
            try:
                ResourceShare.query.filter_by(ResourceId=requirement.Id, ResourceType='r', ShareDomainId=0).one()
            except NoResultFound:
                r = ResourceShare(requirement.Id, 'r', 0)
                db.session.add(r)

    db.session.commit()
    return requirement


@moudule.route('/specifyProducers', methods=['GET', 'POST'])   # 不用了
@output_data
@PermissionValidate()
def specifyProducers():
    param = request.json_param
    ResourceShare.query.filter_by(ResourceId=param[u'reqId'], ResourceType='r').delete()
    if len(param[u'specifyProducers']) > 0:
        for domainId in param[u'specifyProducers']:
            r = ResourceShare(param[u'reqId'], 'r', domainId)
            db.session.add(r)
    else:
        try:
            ResourceShare.query.filter_by(ResourceId=param[u'reqId'], ResourceType='r', ShareDomainId=0).one()
        except NoResultFound:
            r = ResourceShare(param[u'reqId'], 'r', 0)
            db.session.add(r)
    db.session.commit()
    return {}


@moudule.route('/delRequirementAttachment', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def delRequirementAttachment():
    session = request.session
    param = request.json_param
    try:
        attachment = RequirementAttachment.query.filter_by(Id=param[u'AttachmentId']).one()
    except NoResultFound:
        raise APIException(DataErrorCode.NoRecord, u'附件数据不存在')
    objectOperatePermission(attachment.ObjectId, session['UserId'], 'requirementAttachment', 'delete')
    db.session.delete(attachment)
    db.session.commit()
    return {u'success': True}


# @moudule.route('/requirements', methods=['GET', 'POST'])
# @PermissionValidate()
# @output_data_without_attribute([])
# @output_data
# def requirements():
#     session = request.session
#     param = request.json_param
#
#     page = 1
#     per_page = 20
#     try:
#         page = param[u'Page']
#         per_page = param[u'PageStep']
#     except KeyError:
#         pass
#
#     # 获取指定需求
#     if u'Id' in param:
#         req = Requirement.query.filter(Requirement.Id == param[u'Id']).all()
#     # 获取多个需求
#     else:
#         # 基本查询语句
#         pagination = Requirement.query.join(ResourceShare, ResourceShare.ResourceId == Requirement.Id)\
#             .filter(ResourceShare.ResourceType == 'r')\
#             .filter(or_(ResourceShare.ShareDomainId == 0, ResourceShare.ShareDomainId == session['DomainId']))
#         if u'SearchKeyword' in param:
#             search_phase = "%" + param[u'SearchKeyword'] + "%"
#             pagination = pagination.filter(Requirement.Title.like(search_phase))
#
#         # 找到服务商关注的需求
#         rf = RequirementFollower.query.filter_by(FollowerDomainId=session['DomainId']).all()
#         req_ids = []
#         for v in rf:
#             req_ids.append(v.RequirementId)
#         # 只查询和当前服务商相关的需求
#         if param[u'filter'] == 'mine':
#             pagination = pagination.filter(Requirement.Id.in_(req_ids))\
#                 .filter(Requirement.Status >= RequirementStatus.Published)
#         # 查询已申请的需求
#         elif param[u'filter'] == 'applyed':
#             pagination = pagination.filter(Requirement.Id.in_(req_ids))\
#                 .filter(Requirement.Status == RequirementStatus.Published)
#         # 查询进行中的需求
#         elif param[u'filter'] == 'working':
#             pagination = pagination.filter(Requirement.Id.in_(req_ids))\
#                 .filter(Requirement.Status > RequirementStatus.Published)\
#                 .filter(Requirement.Status != RequirementStatus.Last)
#         # 查询已完成的需求
#         elif param[u'filter'] == 'complete':
#             pagination = pagination.filter(Requirement.Id.in_(req_ids))\
#                 .filter(Requirement.Status == RequirementStatus.Last)
#         # 查询所有提交的需求
#         elif param[u'filter'] == 'all':
#             pagination = pagination.filter(Requirement.Id.notin_(req_ids))\
#                 .filter(Requirement.Status == RequirementStatus.Published)
#         # 查询服务商未申请的需求
#         elif param[u'filter'] == 'notCare':
#             pagination = pagination.filter(Requirement.Id.notin_(req_ids))\
#                 .filter(Requirement.Status == RequirementStatus.Published)
#
#         # 过滤需求类型
#         if int(param[u'Category1']):
#             pagination = pagination.filter(Requirement.Category_1 == int(param[u'Category1']))
#         if int(param[u'Category2']):
#             pagination = pagination.filter(Requirement.Category_2 == int(param[u'Category2']))
#         # 以创建时间倒序，分页
#         pagination = pagination.order_by(Requirement.CreateTime.desc()).paginate(page, per_page)
#         req = pagination.items
#         req = expandAttribute(req, [])
#         # 查询服务商对每个需求的申请状态
#         for r in req:
#             r['applyed'] = False
#             for v in rf:
#                 if r['Id'] == v.RequirementId:
#                     r['applyed'] = True
#                     break
#
#     #依据资源共享内容过滤需求
#     result = req
#     if u'Id' in param:
#         result = expandAttribute(result, ['RequirementAttachment', 'Contract'])
#         result[0]['follower'] = getRequirementFollower_p(param[u'Id'], session['DomainId'])
#
#         # 取参考视频的文件名
#         result[0]['referName'] = result[0]['Refer']
#         refer = result[0]['Refer']
#         npos = refer.rfind('/')
#         if npos is not -1:
#             refer = int(refer[npos+1:len(refer)])
#             try:
#                 referObj = Object.query.filter_by(Id=refer).one()
#                 referName = referObj.Name
#                 result[0]['referName'] = referName
#             except NoResultFound:
#                 pass
#
#         # 取留言信息
#         # if req[0].ServiceUserId:
#         #     try:
#         #         group = RequirementReplyGroup.query.filter_by(RequirementId=param[u'Id'], ServiceDomainId=req[0].ServiceUser.DomainId).one()
#         #         replys = db.session.query(RequirementReply).filter(RequirementReply.ReplyGroup == group.Id)\
#         #             .order_by(RequirementReply.CreateTime).all()
#         #         result[0]['replys'] = expandAttribute(replys, ['Publisher'])
#         #     except NoResultFound:
#         #         pass
#
#         try:
#             c1 = Category.query.filter_by(Id=result[0]['Category_1']).one()
#             c2 = Category.query.filter_by(Id=result[0]['Category_2']).one()
#             result[0]['Type'] = c1.Name + '+' + c2.Name
#         except NoResultFound:
#             pass
#         return result
#     else:
#         c1 = Category.query.filter_by(Level=1).all()
#         c2 = Category.query.filter_by(Level=2).all()
#         return {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': result,
#                 'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
#                 'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num,
#                 'Category1': c1, 'Category2': c2}

@moudule.route('/requirements', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def requirements():
    session = request.session
    param = request.json_param

    if u'Id' in param: # 获取指定需求
        result = Requirement.query.filter(Requirement.Id == param[u'Id']).all()
        result = expandAttribute(result, ['RequirementAttachment', 'Contract'])

        # 该需求与自己相关的方案
        result[0]['follower'] = getRequirementFollower_p(param[u'Id'], session['DomainId'])

        # 取参考视频的文件名
        refer = result[0]['Refer']
        npos = refer.rfind('/')
        if npos is not -1:
            id = int(refer[npos+1:len(refer)])
            try:
                refer = Object.query.filter_by(Id=id).one().name
            except NoResultFound:
                pass
        result[0]['referName'] = refer

        # 需求类型
        try:
            c1 = Category.query.filter_by(Id=result[0]['Category_1']).one()
            c2 = Category.query.filter_by(Id=result[0]['Category_2']).one()

            result[0]['Type'] = c1.Name + '+' + c2.Name
        except NoResultFound:
            pass

        return result
    else:   # 获取多个需求
        page = 1
        per_page = 20
        try:
            page = param[u'Page']
            per_page = param[u'PageStep']
        except KeyError:
            pass

        # 基本查询
        pagination = Requirement.query.join(ResourceShare, ResourceShare.ResourceId == Requirement.Id)\
            .filter(ResourceShare.ResourceType == 'r')\
            .filter(or_(ResourceShare.ShareDomainId == 0, ResourceShare.ShareDomainId == session['DomainId']))

        # 关键字过滤
        if u'SearchKeyword' in param:
            search_phase = "%" + param[u'SearchKeyword'] + "%"
            pagination = pagination.filter(Requirement.Title.like(search_phase))

        # 与自己相关的全部、已申请、进行中、已完成、未申请的过滤
        if param[u'filter'] == 'mine':
            pagination = pagination.filter(Requirement.ServiceUserId == session['UserId'])\
                .filter(Requirement.Status >= RequirementStatus.Published)
        elif param[u'filter'] == 'applyed':
            pagination = pagination.filter(Requirement.ServiceUserId == session['UserId'])\
                .filter(Requirement.Status == RequirementStatus.Published)
        elif param[u'filter'] == 'working':
            pagination = pagination.filter(Requirement.ServiceUserId == session['UserId'])\
                .filter(Requirement.Status > RequirementStatus.Published)\
                .filter(Requirement.Status != RequirementStatus.Last)
        elif param[u'filter'] == 'complete':
            pagination = pagination.filter(Requirement.ServiceUserId == session['UserId'])\
                .filter(Requirement.Status == RequirementStatus.Last)
        elif param[u'filter'] == 'all':
            pagination = pagination.filter(Requirement.ServiceUserId == None)\
                .filter(Requirement.Status == RequirementStatus.Published)

        # 需求类型过滤
        if param[u'Category1'] != None:
            if int(param[u'Category1']) != 0:
                pagination = pagination.filter(Requirement.Category_1 == int(param[u'Category1']))
        if param[u'Category2'] != None:
            if int(param[u'Category2']) != 0:
                pagination = pagination.filter(Requirement.Category_2 == int(param[u'Category2']))

        # 以创建时间倒序，分页
        pagination = pagination.order_by(Requirement.CreateTime.desc()).paginate(page, per_page)

        # 扩充属性及更新状态
        result = expandAttribute(pagination.items, [])
        for r in result:
            r['applyed'] = False
            if r['ServiceUserId'] == session['UserId']:
                r['applyed'] = True

        return {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': result,
                'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
                'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num,
                'Category1': param[u'Category1'], 'Category2': param[u'Category2']}


@moudule.route('/requirement', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def requirement():
    param = request.json_param
    try:
        req = Requirement.query.filter(Requirement.Id == param[u'Id']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'无该需求数据')
    result = expandAttribute(req, ['RequirementAttachment'])
    return result


@moudule.route('/myRequirements', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def myRequirements():
    session = request.session
    param = request.json_param

    if u'Id' in param: # 取单个需求
        result = Requirement.query.filter(Requirement.Id == param[u'Id']).all()
        result = expandAttribute(result, ['RequirementAttachment', 'Contract'])

        # 申请该需求的制作商（ID,昵称）
        result[0]['replyUsers'] = []
        replyUsers = db.session.query(RequirementReply.PublisherId.distinct(), User.NickName)\
            .join(User, User.Id == RequirementReply.PublisherId)\
            .filter(and_(RequirementReply.RequirementId == param[u'Id'],
                         RequirementReply.PublisherId != session['UserId'])).all()
        for user in replyUsers:
            result[0]['replyUsers'].append({'Id': user[0], 'NickName': user[1]})

        # 与需求相关的方案
        result[0]['follower'] = getRequirementFollower_p(param[u'Id'], session['DomainId'])

        # 取参考视频的文件名
        refer = result[0]['Refer']
        npos = refer.rfind('/')
        if npos is not -1:
            id = int(refer[npos+1:len(refer)])
            try:
                obj = Object.query.filter_by(Id=id).one()
                if obj != None:
                    refer = obj.Name
            except NoResultFound:
                pass
        result[0]['referName'] = refer

        # 需求类型
        try:
            c1 = Category.query.filter_by(Id=result[0]['Category_1']).one()
            c2 = Category.query.filter_by(Id=result[0]['Category_2']).one()

            result[0]['Type'] = c1.Name + '+' + c2.Name
        except NoResultFound:
            pass

        # 指定的制作商
        result[0]['specifyProducers'] = {}
        domains = db.session.query(Domain).join(ResourceShare, ResourceShare.ShareDomainId == Domain.Id)\
            .filter(ResourceShare.ResourceId == result[0]['Id'])\
            .filter(ResourceShare.ResourceType == 'r').all()
        for d in domains:
            result[0]['specifyProducers'][d.Id] = d

        return result
    else: # 取需求列表
        page = 1
        per_page = 20
        try:
            page = param[u'Page']
            per_page = param[u'PageStep']
        except KeyError:
            pass

        # 获取该用户提的需求
        pagination = Requirement.query.join(User, Requirement.PublisherId == User.Id)\
            .filter(User.DomainId == session['DomainId'])

        # 关键字过滤
        if u'SearchKeyword' in param:
            search_phase = "%" + param[u'SearchKeyword'] + "%"
            pagination = pagination.filter(Requirement.Title.like(search_phase))

        # 状态过滤
        if param[u'filter'] == 'all':
            pagination = pagination.filter(Requirement.Status == RequirementStatus.Published)
        elif param[u'filter'] == 'edit':
            pagination = pagination.filter(and_(Requirement.Status > RequirementStatus.Published,
                                                Requirement.Status < RequirementStatus.Last))
        elif param[u'filter'] == 'finish':
            pagination = pagination.filter(Requirement.Status == RequirementStatus.Last)
        elif param[u'filter'] == 'draft':
            pagination = pagination.filter(Requirement.Status == RequirementStatus.Created)

        # 分页、倒序排列
        pagination = pagination.order_by(Requirement.CreateTime.desc()).paginate(page, per_page)
        result = pagination.items
        result = expandAttribute(result, [])

        return {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': result,
                'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
                'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num, 'CurUserId':session['UserId']}


@moudule.route('/requirementReply', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def requirementReply():
    param = request.json_param
    try:
        user = User.query.filter_by(Id=param[u'PublisherId']).one()
    except NoResultFound:
        return APIException(DataErrorCode.NoRecord, u'无留言')
    try:
        group = RequirementReplyGroup.query.filter_by(RequirementId=param[u'Id'], ServiceDomainId=user.DomainId, FollowerId=param[u'FollowerId']).one()
    except NoResultFound:
        return []

    result = db.session.query(RequirementReply)\
        .filter(RequirementReply.ReplyGroup == group.Id)\
        .order_by(RequirementReply.CreateTime).all()
    result = expandAttribute(result, ['Publisher'])
    return result


@moudule.route('/publishRequirementReply', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def publishRequirementReply():
    session = request.session
    param = request.json_param

    destUser = User.query.filter_by(Id=param[u'DestUserId']).one()
    if session['IsService']:
        serviceDomainId = session['DomainId']
        try:
            RequirementFollower.query.filter_by(FollowerDomainId=session['DomainId'], RequirementId=param[u'RequirementId'], Id=param[u'FollowerId']).one()
        except NoResultFound:
            return {'failed': True}
    else:
        serviceDomainId = destUser.DomainId

    try:
        group = RequirementReplyGroup.query.filter_by(RequirementId=param[u'RequirementId'], ServiceDomainId=serviceDomainId, FollowerId=param[u'FollowerId']).one()
    except NoResultFound:
        group = RequirementReplyGroup(param[u'RequirementId'], serviceDomainId, param[u'FollowerId'])
        db.session.add(group)
        db.session.flush()

    reply = RequirementReply()
    reply.PublisherId = session['UserId']
    reply.RequirementId = param[u'RequirementId']
    reply.Reply = param[u'Reply']
    reply.Status = RequirementReplyStatus.First
    reply.ReplyGroup = group.Id
    db.session.add(reply)

    req = Requirement.query.filter_by(Id=param[u'RequirementId']).one()
    log = '用户\"' + session['CompanyName'] + '\"在需求\"' + req.Title + '\"中给您留言：\"' + reply.Reply + '\"'
    try:
        pm = PlatformMsg.query.filter_by(ResourceId=reply.RequirementId, SrcUserId=session['UserId'],
                                         DestUserId=destUser.Id, ResourceType='requirement', MsgType='reply').one()
        pm.Msg = log
        pm.IsAdopted = 0
        pm.IsReaded = 0
    except NoResultFound:
        pm = PlatformMsg('新留言', log, session['UserId'], destUser.Id, reply.RequirementId, 'requirement', 'reply')
        db.session.add(pm)

    db.session.commit()
    return reply


@moudule.route('/requirementLog', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def requirementLog():
    session = request.session
    logs = db.session.query(PlatformMsg).filter(PlatformMsg.ResourceType == 'requirement')\
        .filter(PlatformMsg.DestUserId == session['UserId'])\
        .order_by(PlatformMsg.CreateTime.desc()).all()
    if session['IsService']:
        pagination = Requirement.query.join(ResourceShare, ResourceShare.ResourceId == Requirement.Id)\
            .filter(Requirement.Status == RequirementStatus.Published)\
            .filter(ResourceShare.ResourceType == 'r')\
            .filter(or_(ResourceShare.ShareDomainId == 0, ResourceShare.ShareDomainId == session['Domain']))\
            .order_by(Requirement.CreateTime.desc()).paginate(1, 5)
        applyCount = RequirementFollower.query.join(Requirement, Requirement.Id == RequirementFollower.RequirementId)\
            .filter(Requirement.Status == RequirementStatus.Published)\
            .filter(RequirementFollower.FollowerDomainId == session['DomainId']).count()
        publishCount = Requirement.query.join(ResourceShare, ResourceShare.ResourceId == Requirement.Id)\
            .filter(Requirement.Status == RequirementStatus.Published)\
            .filter(ResourceShare.ResourceType == 'r')\
            .filter(or_(ResourceShare.ShareDomainId == 0, ResourceShare.ShareDomainId == session['DomainId'])).count()
        return {'newPublish': pagination.items, 'logs': logs, 'applyCount': applyCount, 'publishCount': publishCount}
    return logs


@moudule.route('/askRequirement', methods=['GET', 'POST'])   #   申请需求并锁定
@PermissionValidate()
@output_data
def askRequirement():
    session = request.session
    param = request.json_param
    try:
        requirement = Requirement.query.filter_by(Id=param[u'ReqId']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'无该需求数据')

    if u'Command' not in param:
        raise APIException(SystemErrorCode.UnkonwnError, u'错误命令')

    if param[u'Command'] == u'ask':
        if requirement.ServiceUserId is not None and requirement.ServiceUserId != session['UserId']:
            raise APIException(SystemErrorCode.UnkonwnError, u'该需求已被他人申请了')
        requirement.ServiceUserId = session['UserId']
        requirement.Status = RequirementStatus.Contracting
        db.session.commit()
        return {'message': u'申请成功'}
    elif param[u'Command'] == u'cancel':
        if requirement.ServiceUserId != session['UserId']:
            raise APIException(SystemErrorCode.UnkonwnError, u'没有申请该需求')
        requirement.ServiceUserId = None
        requirement.Status = RequirementStatus.Published
        db.session.commit()
        return {'message': u'取消成功'}
    else:
        raise APIException(SystemErrorCode.UnkonwnError, u'错误命令')



@moudule.route('/addRequirementFollower', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def addRequirementFollower():
    session = request.session
    param = request.json_param
    try:
        requirement = Requirement.query.filter_by(Id=param[u'ReqId']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'无该需求数据')

    rf = RequirementFollower(param[u'ReqId'], session['UserId'], session['DomainId'])
    db.session.add(rf)
    log = '制作商\"' + session['CompanyName'] + '\"申请了您提交的制作需求\"' + requirement.Title + '\"'
    pm = PlatformMsg('申请', log, session['UserId'], requirement.Publisher.Id, param[u'ReqId'], 'requirement', 'focus')
    db.session.add(pm)
    db.session.commit()
    return rf


@moudule.route('/reapplyRequirementFollower', methods=['GET', 'POST'])  # 重新申请用户deny的方案
@PermissionValidate()
@output_data
def reapplyRequirementFollower():
    param = request.json_param
    session = request.session

    req = Requirement.query.filter_by(Id=param[u'ReqId']).one()
    rf = RequirementFollower.query.filter_by(RequirementId=param[u'ReqId'], Id=param[u'FollowerId']).one()

    rf.IsDeny = False
    log = rf.Follower.Domain.CompanyName + '\"修改了\"' + req.Title + '\"的方案，并重新申请\"'
    pm = PlatformMsg('重新申请', log, session['UserId'], req.PublisherId, param[u'ReqId'], 'requirement', 'cancelFocus')
    db.session.add(pm)
    db.session.commit()
    return {'reapply': True}


@moudule.route('/removeRequirementFollower', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def removeRequirementFollower():
    param = request.json_param
    session = request.session
    if u'Id' in param:
        req = Requirement.query.filter_by(Id=param[u'ReqId']).one()
        rf = RequirementFollower.query.filter_by(RequirementId=param[u'ReqId'], Id=param[u'Id']).one()
        if u'Deny' in param:
            rf.IsDeny = True
            log = '用户\"' + rf.Follower.Domain.CompanyName + '\"取消了您对他制作需求\"' + req.Title + '\"的申请'
            pm = PlatformMsg('取消申请', log, session['UserId'], rf.Follower.Id, param[u'ReqId'], 'requirement', 'cancelFocus')
            db.session.add(pm)
        else:
            db.session.delete(rf)
    else:
        return {'delete': False}
    #     rf = RequirementFollower.query.filter_by(RequirementId=param[u'ReqId']).all()
    #     db.session.delete(rf)
    db.session.commit()
    return {'delete': True}


@moudule.route('/getRequirementFollower', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getRequirementFollower():
    session = request.session
    param = request.json_param
    reqId = param[u'ReqId']
    domainId = session['DomainId']

    if u'FollowerId' in param:
        if session['IsService']:
            rf = RequirementFollower.query.filter_by(RequirementId=reqId, FollowerDomainId=domainId, Id=param[u'FollowerId']).all()
        else:
            rf = RequirementFollower.query.filter_by(RequirementId=reqId, IsDeny=0, Id=param[u'FollowerId']).all()
    else:
        if session['IsService']:
            rf = RequirementFollower.query.filter_by(RequirementId=reqId, FollowerDomainId=domainId).all()
        else:
            rf = RequirementFollower.query.filter_by(RequirementId=reqId, IsDeny=0).all()
    return rf


def getRequirementFollower_p(reqId, domainId):
    session = request.session
    if session['IsService']:
        rf = RequirementFollower.query.filter_by(RequirementId=reqId, FollowerDomainId=domainId).all()
    else:
        rf = RequirementFollower.query.filter_by(RequirementId=reqId, IsDeny=0).all()
    return rf


@moudule.route('/saveReqScheme', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveReqScheme():
    session = request.session
    param = request.json_param
    try:
        rf = RequirementFollower.query.filter_by(RequirementId=param[u'ReqId'],
                                                 FollowerDomainId=session['DomainId'], Id=param[u'Id']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无法修改需求方案，无该制作商的需求申请记录')
    if u'long' in param:
        rf.Long = param[u'Long']
    rf.Format = param[u'Format']
    # rf.Subtitle = param[u'SubTitle']
    # rf.Voice = param[u'Voice']
    # rf.Gbm = param[u'Gbm']
    if param[u'BasePrice'] == '':
        rf.BasePrice = 0
    else:
        rf.BasePrice = round_(float(param[u'BasePrice']))
    if param[u'SchemePrice'] == '':
        rf.SchemePrice = 0
    else:
        rf.SchemePrice = round_(float(param[u'SchemePrice']))
    if param[u'ShotPrice'] == '':
        rf.ShotPrice = 0
    else:
        rf.ShotPrice = round_(float(param[u'ShotPrice']))
    if param[u'ActorPrice'] == '':
        rf.ActorPrice = 0
    else:
        rf.ActorPrice = round_(float(param[u'ActorPrice']))
    if param[u'MusicPrice'] == '':
        rf.MusicPrice = 0
    else:
        rf.MusicPrice = round_(float(param[u'MusicPrice']))
    if param[u'AEPrice'] == '':
        rf.AEPrice = 0
    else:
        rf.AEPrice = round_(float(param[u'AEPrice']))
    rf.Amount = rf.BasePrice + rf.SchemePrice + rf.ShotPrice + rf.ActorPrice + rf.MusicPrice + rf.AEPrice
    if rf.Amount < 0:
        rf.Amount = 0
    rf.Script = param[u'Script']
    rf.DepositPercent = param[u'DepositPercent']
    # rf.Remark = param[u'Remark']

    req = Requirement.query.filter_by(Id=param[u'ReqId']).one()
    log = '制作商\"' + session['CompanyName'] + '\"修改了需求\"' + req.Title + '\"的制作方案'
    pm = PlatformMsg('修改制作方案', log, session['UserId'], req.PublisherId, param[u'ReqId'], 'requirement', 'modifyScheme')
    db.session.add(pm)

    db.session.commit()
    return rf


@moudule.route('/applyReqScheme', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def applyReqScheme():
    session = request.session
    param = request.json_param
    try:
        rf = RequirementFollower.query.filter_by(RequirementId=param[u'ReqId'], Id=param[u'Id']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无法修改需求方案，无该制作商的需求申请记录')
    rf.Status = param[u'Status']
    r = Requirement.query.filter_by(Id=param[u'ReqId']).one()
    if param[u'Status']:
        log = '制作商\"' + rf.Follower.Domain.CompanyName + '\"申请方案确认，请注意查看'
        pm = PlatformMsg('方案确认申请', log, session['UserId'], r.Publisher.Id, r.Id, 'requirement', 'apply')
    else:
        log = '客户拒绝了您对需求\"' + r.Title + '\"的方案申请，请注意查看'
        pm = PlatformMsg('需求方案审核未通过', log, session['UserId'], rf.FollowerProducerId, r.Id, 'requirement', 'apply')
    db.session.add(pm)
    db.session.commit()
    return rf


@moudule.route('/saveReqScript', methods=['GET', 'POST'])  #  无用了
@PermissionValidate()
@output_data
def saveReqScript():
    session = request.session
    param = request.json_param
    try:
        rf = RequirementFollower.query.filter_by(RequirementId=param[u'ReqId'], FollowerDomainId=session['DomainId'], Id=param[u'FollowerId']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无法修改需求方案，无该制作商的需求申请记录')
    rf.Script = param[u'Content']
    db.session.commit()
    return rf

@moudule.route('/finishComment', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def finishComment():
    param = request.json_param
    requirement = Requirement.query.filter_by(Id=param[u'reqId']).one()
    requirement.Star = param[u'star']
    requirement.Comment = param[u'comment']
    db.session.commit()
    return

@moudule.route('/applyContract', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def applyContract():
    session = request.session
    param = request.json_param
    try:
        requirement = Requirement.query.filter_by(Id=param[u'RequirementId']).one()
        serviceUser = User.query.filter_by(Id=param[u'ServiceUserId']).one()
        user = User.query.filter_by(Id=session['UserId']).one()
        rf = RequirementFollower.query.filter_by(Id=param[u'FollowerId']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'数据不存在')
    # 缺少某一个属性,也就是RequirementStatus没有contracting属性

    # if requirement.Status != RequirementStatus.contracting:

    #     raise APIException(SystemErrorCode.UnkonwnError, u'需求已经开始制作')

    requirement.Long = rf.Long
    requirement.Format = rf.Format
    requirement.Subtitle = rf.Subtitle
    requirement.Voice = rf.Voice
    requirement.Gbm = rf.Gbm
    requirement.Amount = rf.Amount
    requirement.Scheme = rf.Scheme
    requirement.DepositPercent = rf.DepositPercent
    requirement.Status = RequirementStatus.PayDeposit
    requirement.ServiceUserId = param[u'ServiceUserId']

    rs = RequirementSegment.query.filter_by(RequirementId=requirement.Id).all()
    if len(rs) == 0:
        rs = RequirementSegment(requirement.Id, RequirementStatus.Published)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.Contracting)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.PayDeposit)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.Reviewing)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.PayAll)
        db.session.add(rs)
        rs = RequirementSegment(requirement.Id, RequirementStatus.Retainage)
        db.session.add(rs)

    if Contract.query.filter(Contract.ServiceUserId == session['UserId']).\
            filter(Contract.RequirementId == param[u'RequirementId']).count() > 0:
        raise APIException(SystemErrorCode.UnkonwnError, u'已经申请过，请勿重新申请')
    contract = Contract()
    contract.ServiceUserId = param[u'ServiceUserId']
    contract.RequirementId = requirement.Id
    contract.CustomerUserId = requirement.PublisherId
    contract.Title = requirement.Title
    contract.Detail = requirement.Detail
    contract.Status = ContractStatus.Established
    contract.Version = 0
    contract.Amount = rf.Amount
    contract.Scheme = rf.Scheme
    contract.DepositPercent = rf.DepositPercent
    db.session.add(contract)
    db.session.flush()

    group = ContractUserGroup(contract.Id, serviceUser.Id, serviceUser.DomainId, '需求申请者')
    db.session.add(group)
    group = ContractUserGroup(contract.Id, user.Id, user.DomainId, '合同建立者')
    db.session.add(group)

    order = Order(str(uuid4()), '合同押金', '合同押金支付，开启视频制作项目',
                  round_(contract.Amount * contract.DepositPercent / 100), contract.CustomerUserId, contract.ServiceUserId)
    db.session.add(order)
    db.session.flush()
    log = '需求方\'' + user.Domain.CompanyName + '\',制作商\'' + \
          serviceUser.Domain.CompanyName + '\'的合同：\'' + contract.Title + '\'进入支付押金阶段，押金订单已建立'
    orderLog = OrderLog(order.Id, '合同押金', log, '订单建立')
    db.session.add(orderLog)
    contractOrder = ContractOrder(contract.Id, order.Id, ContractOrderType.PayRent)
    db.session.add(contractOrder)
    requirement.ContractId = contract.Id
    db.session.commit()
    return {}

    # contractseg = ContractSegment()
    # contractseg.Remark = u'创建合同'
    # contractseg.Deadline = datetime(1000, 1, 1)
    # contractseg.ApplyUserId = contract.ServiceUserId
    # contractseg.ApplyTime = datetime.now()
    # contractseg.ApplyRemark = '我申请了您的视频制作需求'
    #     # param[u'ApplyRemark']
    # contractseg.Status = ContractSegmentStatus.Applied
    # contractseg.Segment = ContractSegmentType.Apply
    # contractseg.ServiceResponser = contract.ServiceUserId
    # contractseg.CustomerResponser = contract.CustomerUserId
    # contract.ContractSegmentDynamic.append(contractseg)
    # db.session.add(contractseg)

    # requirement.Status = RequirementStatus.Contracting
    # log = '用户\"' + user.Domain.CompanyName + '\"同意与您针对需求\"' + requirement.Title + '\"进行合同协商，请积极配合'
    # pm = PlatformMsg('协商合同', log, session['UserId'], serviceUser.Id, contract.Id, 'contract', 'negotiation')
    # db.session.add(pm)
    # RequirementFollower.query.filter_by(RequirementId=param[u'RequirementId']).delete()

    # return contract
@moudule.route('/denyDeposit', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def denyDeposit():
    session = request.session
    param = request.json_param
    try:
        requirement = Requirement.query.filter_by(Id=param[u'RequirementId']).one()
        serviceUser = User.query.filter_by(Id=param[u'ServiceUserId']).one()
        user = User.query.filter_by(Id=session['UserId']).one()
    except NoResultFound:
        raise APIException(SystemErrorCode.UnkonwnError, u'数据不存在')
    if requirement.Status != RequirementStatus.PayDeposit:
        raise APIException(SystemErrorCode.UnkonwnError, u'需求不处于支付押金的环节')

    requirement.Status = RequirementStatus.Published
    requirement.ServiceUserId = None
    requirement.ContractId = None

    RequirementSegment.query.filter_by(RequirementId=requirement.Id).delete()
    contract = Contract.query.filter_by(RequirementId=requirement.Id).one()
    ContractUserGroup.query.filter_by(ContractId=contract.Id).delete()
    cOrder = ContractOrder.query.filter_by(ContractId=contract.Id).one()
    order = Order.query.filter_by(Id=cOrder.OrderId).one()
    OrderLog.query.filter_by(OrderId=order.Id).delete()

    db.session.delete(cOrder)
    db.session.delete(order)
    db.session.delete(contract)
    log = '需求方\"' + user.Domain.CompanyName + '\"将需求\"' + contract.Title + '\"回退到需求协商阶段，请关注！'
    pm = PlatformMsg('用户回退', log, session['UserId'], serviceUser.Id, requirement.Id, 'requirement', 'goback')
    db.session.add(pm)
    db.session.commit()
    return {}


# 拒绝和该服务商建立合同
@moudule.route('/denyContract', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def denyContract():
    param = request.json_param
    try:
        contract = Contract.query.filter_by(Id=param[u'ContractId']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无留言')

    if contract.Status == ContractStatus.ContractModifying:
        req = Requirement.query.filter_by(Id=contract.RequirementId).one()
        req.Status = RequirementStatus.Published
        ContractSegmentLog.query.filter_by(ContractId=contract.Id).delete()
        ContractSegment.query.filter_by(ContractId=contract.Id).delete()
        ContractUserGroup.query.filter_by(ContractId=contract.Id).delete()
        ContractAttachment.query.filter_by(ContractId=contract.Id).delete()
        ContractReply.query.filter_by(ContractId=contract.Id).delete()
        ContractEventLog.query.filter_by(ContractId=contract.Id).delete()
        ContractHistory.query.filter_by(ContractId=contract.Id).delete()
        db.session.delete(contract)

    db.session.commit()
    return {"result": "done"}


@moudule.route('/editContractUser', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def editContractUser():
    session = request.session
    param = request.json_param

    contractId = param[u'ContractId']
    if param[u'Operator'] == 'add':
        for userId in param[u'UsersId']:
            try:
                ContractUserGroup.query.filter_by(ContractId=contractId, UserId=userId).one()
            except NoResultFound:
                cug = ContractUserGroup(contractId, userId, session['DomainId'], '')
                db.session.add(cug)
                db.session.flush()
    elif param[u'Operator'] == 'del':
        if session['IsService']:
            ContractSegment.query.filter_by(ContractId=contractId, ServiceResponser=param[u'UserId']).update({'ServiceResponser': None})
        else:
            ContractSegment.query.filter_by(ContractId=contractId, CustomerResponser=param[u'UserId']).update({'ServiceResponser': None})
        ContractUserGroup.query.filter_by(ContractId=contractId, UserId=param[u'UserId']).delete()
    elif param[u'Operator'] == 'modify':
        cug = ContractUserGroup.query.filter_by(ContractId=contractId, UserId=param[u'UserId']).one()
        cug.Description = param[u'Description']

    db.session.commit()
    return ContractUserGroup.query.filter_by(ContractId=contractId).all()


@moudule.route('/specifySegmentResponser', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def specifySegmentResponser():
    session = request.session
    param = request.json_param
    seg = ContractSegment.query.filter_by(Id=param[u'SegmentId']).one()
    if session['IsService']:
        seg.ServiceResponser = param[u'UserId']
    else:
        seg.CustomerResponser = param[u'UserId']
    db.session.commit()
    return ContractUserGroup.query.filter_by(ContractId=seg.ContractId, UserId=param[u'UserId']).one()


@moudule.route('/publishContractReply', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def publishContractReply():
    session = request.session
    param = request.json_param
    reply = ContractReply()
    reply.PublisherId = session['UserId']
    reply.ContractId = param[u'ContractId']
    reply.Reply = param[u'Reply']
    if u'DestUserId' in param:
        reply.DestUserId = param[u'DestUserId']
    reply.Status = RequirementReplyStatus.NewPublishedNext
    db.session.add(reply)

    c = Contract.query.filter_by(Id=param[u'ContractId']).one()
    user = User.query.filter_by(Id=session['UserId']).one()
    log = '用户\"' + user.DomainName + '\"在合同\"' + c.Title + '\"给您留言：\"' + reply.Reply + '\"'
    clog = ContractEventLog(param[u'ContractId'], session['UserId'], ContractLogActionType.Reply, 0, log)
    db.session.add(clog)
    db.session.flush()
    if u'DestUserId' not in param:
        groupUsers = ContractUserGroup.query.filter_by(ContractId=param[u'ContractId']).all()
        for u in groupUsers:
            if u.UserId != session['UserId']:
                try:
                    pm = PlatformMsg.query.filter_by(ResourceId=param[u'ContractId'], ResourceType='contract',
                                                     MsgType='reply', SrcUserId=session['UserId'], DestUserId=u.UserId).one()
                    pm.Msg = log
                    pm.IsAdopted = 0
                    pm.IsReaded = 0
                except NoResultFound:
                    pm = PlatformMsg('新留言', log, session['UserId'], u.UserId, param[u'ContractId'], 'contract', 'reply')
                    db.session.add(pm)
    else:
        u = User.query.filter_by(Id=param[u'DestUserId']).one()
        try:
            pm = PlatformMsg.query.filter_by(ResourceId=param[u'ContractId'], ResourceType='contract',
                                             MsgType='reply', SrcUserId=session['UserId'], DestUserId=u.Id).one()
            pm.Msg = log
            pm.IsAdopted = 0
            pm.IsReaded = 0
        except NoResultFound:
            pm = PlatformMsg('新留言', log, session['UserId'], u.Id, param[u'ContractId'], 'contract', 'reply')
            db.session.add(pm)

    db.session.commit()
    return reply


@moudule.route('/contractReply', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def contractReply():
    session = request.session
    param = request.json_param
    try:
        if u'UserId' not in param:
            result = db.session.query(ContractReply).filter(ContractReply.ContractId == param[u'Id'])\
                .filter(ContractReply.DestUserId == None).order_by(ContractReply.CreateTime.desc()).all()
        else:
            result = ContractReply.query.filter(and_(ContractReply.ContractId == param[u'Id'],
                                                     or_(and_(ContractReply.DestUserId == param[u'UserId'],
                                                              ContractReply.PublisherId == session['UserId']),
                                                         and_(ContractReply.DestUserId == session['UserId'],
                                                              ContractReply.PublisherId == param[u'UserId']))))\
                .order_by(ContractReply.CreateTime.desc()).all()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无留言')
    result = expandAttribute(result, ['Publisher'])
    return result


@moudule.route('/getAllContract', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def getAllContract():
    contract = Contract.query.all()
    return contract


@moudule.route('/getContractByReq', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def getContractByReq():
    param = request.json_param
    try:
        contract = Contract.query.filter_by(RequirementId=param[u'ReqId']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无对应合同')
    return contract


@moudule.route('/getContractLog', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def getContractLog():
    session = request.session
    logs = db.session.query(PlatformMsg).filter(PlatformMsg.ResourceType == 'contract')\
        .filter(PlatformMsg.DestUserId == session['UserId']).all()
    return logs


@moudule.route('/modifyContractPayState', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def modifyContractPayState():
    param = request.json_param
    contract = Contract.query.filter(Contract.Id == param[u'ContractId']).one()
    contract.PayState = 1
    db.session.commit()
    return contract


@moudule.route('/myContract', methods=['GET', 'POST'])
@PermissionValidate()
@output_data_without_attribute([])
@output_data
def myContract():
    session = request.session
    param = request.json_param
    user = User.query.filter_by(Id=session['UserId']).one()
    if u'Load'in param:
        contract = Contract.query.filter(Contract.Id == param[u'Id']).one()
        contract.Status = 1
        contract.CustomerUserId = param[u'CustomerUserId']
        contract.Amount = param[u'Amount']
        contract.Detail = param[u'Detail']

        if user.DomainId is None:
            if contract.Requirement.PublisherId != user.Id:
                raise APIException(SystemErrorCode.UnkonwnError, u'需求提交者确认合同后才可修改合同')
        elif contract.Requirement.Publisher.DomainId != user.DomainId:
            raise APIException(SystemErrorCode.UnkonwnError, u'需求提交者确认合同后才可修改合同')

        contract.Status = ContractStatus.ContractAppliedNext
        contract.Requirement.Status = RequirementStatus.PublishedNext
        conseg = contract.ContractSegment[0]
        conseg.ConfirmUserId = session['UserId']
        conseg.ConfirmTime = datetime.now()
        conseg.ConfirmRemark = u'创建完成'
        conseg.ApplyRemark = u'创建完成'
        conseg.Status = ContractSegmentStatus.Confirmed
        contractseg = ContractSegment()
        contractseg.Remark = u'商订合同'
        contractseg.Deadline = datetime.now()
        contractseg.Segment = ContractSegmentType.Establish
        contractseg.Status = ContractSegmentStatus.Init
        contractseg.ServiceResponser = contract.ServiceUserId
        contractseg.CustomerResponser = contract.CustomerUserId
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)

        contractseg = ContractSegment()
        contractseg.Remark = u'支付押金'
        contractseg.Deadline = datetime.now()
        contractseg.Segment = ContractSegmentType.Start
        contractseg.Status = ContractSegmentStatus.Init
        contractseg.ServiceResponser = contract.ServiceUserId
        contractseg.CustomerResponser = contract.CustomerUserId
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)

        contractseg = ContractSegment()
        contractseg.Remark = u'成片审核'
        contractseg.Deadline = dateutil.parser.parse(contract.Requirement.Deadline)
        contractseg.Segment = ContractSegmentType.Reviewed
        contractseg.Status = ContractSegmentStatus.Init
        contractseg.ServiceResponser = contract.ServiceUserId
        contractseg.CustomerResponser = contract.CustomerUserId
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)

        contractseg = ContractSegment()
        contractseg.Remark = u'支付尾款'
        contractseg.Deadline = dateutil.parser.parse(contract.Requirement.Deadline)
        contractseg.Segment = ContractSegmentType.Complete
        contractseg.Status = ContractSegmentStatus.Init
        contractseg.ServiceResponser = contract.ServiceUserId
        contractseg.CustomerResponser = contract.CustomerUserId
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)

        contractseg = ContractSegment()
        contractseg.Remark = u'交付成片'
        contractseg.Deadline = dateutil.parser.parse(contract.Requirement.Deadline)
        contractseg.Segment = ContractSegmentType.End
        contractseg.Status = ContractSegmentStatus.Init
        contractseg.ServiceResponser = contract.ServiceUserId
        contractseg.CustomerResponser = contract.CustomerUserId
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)

        contract.Version += 1

        contractHistory = ContractHistory()
        contractHistory.ContractId = contract.Id
        contractHistory.Version = contract.Version
        contractHistory.ApplyTime = datetime.now()
        contractHistory.ApplyRemark = "原始版本"
        contractHistory.Detail = contract.Detail
        db.session.add(contractHistory)

        sharetoUsers = User.query.filter_by(DomainId=contract.ServiceUser.DomainId).all()
        for user in sharetoUsers:
            resourceShare = ResourceShare(contract.Id, 'c', user.Id)
            db.session.add(resourceShare)

        db.session.flush()
        db.session.commit()
        contract.Id
        return contract

    if u'Id' in param:
        # 清除相关日志
        try:
            PlatformMsg.query.filter_by(ResourceType='contract', ResourceId=param[u'Id'], DestUserId=session['UserId']).delete()
            db.session.commit()
        except:
            pass

        contract = Contract.query.filter(Contract.Id == param[u'Id']).one()
        # cd = expandAttribute(contract, ['ContractUserGroup:["User"]', 'ContractAttachment:["Share"]','Requirement'])
        cd = expandAttribute(contract, [])
        try:
            cd[u'Deadline'] = contract.ContractSegmentDynamic.filter(
                ContractSegment.Segment == ContractSegmentType.End).one().Deadline
        except NoResultFound:
            pass
        cd['ProjectCount'] = contract.Project.count()
        cd['ContractUserGroup'] = ContractUserGroup.query.filter_by(ContractId=contract.Id).all()
        return cd

    page = 1
    per_page = 10
    try:
        page = param[u'Page']
        per_page = param[u'PageStep']
    except:
        pass

    # if session['IsService']:
    #     resources = ResourceShare.query.filter_by(ShareUserId=session['UserId'], ResourceType='c').all()
    #     resourcesId = []
    #     for r in resources:
    #         resourcesId.append(r.ResourceId)
    #     if u'SearchKeyword' in param:
    #         searchPhase = "%" + param[u'SearchKeyword'] + "%"
    #         pagination = Contract.query.filter(and_(Contract.Id.in_(resourcesId), Contract.Title.like(searchPhase))).\
    #             order_by(Contract.CreateTime.desc()).paginate(page, per_page)
    #     else:
    #         pagination = Contract.query.filter(Contract.Id.in_(resourcesId)).\
    #             order_by(Contract.CreateTime.desc()).paginate(page, per_page)
    #     return {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
    #             'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
    #             'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}
    # else:
    conList = db.session.query(ContractUserGroup.ContractId).filter(ContractUserGroup.UserId == session['UserId']).all()
    conArr = []
    for con in conList:
        for e in con:
            conArr.append(e)
    # domainUsersId = [session['UserId']]
    # Friend = aliased(User, name='Friend')
    # users = db.session.query(Friend.Id)\
    #     .join(User, User.DomainId == Friend.DomainId)\
    #     .filter(and_(User.DomainId is not None, User.Id == session['UserId'])).all()
    # for user in users:
    #     for e in user:
    #         if e == session['UserId']:
    #             continue
    #         domainUsersId.append(e)
    if u'SearchKeyword' in param:
        searchPhase = "%" + param[u'SearchKeyword'] + "%"
        pagination = Contract.query.filter(and_(Contract.Title.like(searchPhase), Contract.Id.in_(conArr)))\
            .order_by(Contract.CreateTime.desc()).paginate(page, per_page)
        # pagination = Contract.query.\
        #     filter(and_(Contract.CustomerUserId.in_(domainUsersId), Contract.Title.like(searchPhase))).\
        #     order_by(Contract.CreateTime.desc()).paginate(page, per_page)
    else:
        pagination = Contract.query.filter(Contract.Id.in_(conArr))\
            .order_by(Contract.CreateTime.desc()).paginate(page, per_page)
        # pagination = Contract.query.filter(Contract.CustomerUserId.in_(domainUsersId)).\
        #     order_by(Contract.CreateTime.desc()).paginate(page, per_page)
    return {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
            'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
            'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}


def addContractAttachment_p(param, session):
    contract = Contract.query.filter_by(Id=param[u'ContractId']).one()
    domainAId = contract.ServiceUser.DomainId
    userAId = contract.ServiceUserId
    domainBId = contract.CustomerUser.DomainId
    userBId = contract.CustomerUserId
    groupAUser = set([user.UserId for user in ContractUserGroup.query.filter(ContractUserGroup.DomainId == domainAId, ContractUserGroup.ContractId == param[u'ContractId']).all()])
    groupBUser = set([user.UserId for user in ContractUserGroup.query.filter(ContractUserGroup.DomainId == domainBId, ContractUserGroup.ContractId == param[u'ContractId']).all()])
    groupAUser.add(userAId)
    groupBUser.add(userBId)
    groupAUser = [{u'Operate': u'add', u"Id": userid} for userid in groupAUser]
    groupBUser = [{u'Operate': u'add', u"Id": userid} for userid in groupBUser]
    groupA = {}
    groupA[u'GroupName'] = u'Contract' + str(contract.Id) + 'Group' + str(domainAId)
    groupA[u'GroupRead'] = 1
    groupA[u'GroupWrite'] = 0
    groupA[u'GroupCreate'] = 0
    groupA[u'GroupDelete'] = 0
    groupA[u'GroupDownload'] = 0
    groupA[u'Users'] = groupAUser
    groupB = {}
    groupB[u'GroupName'] = u'Contract' + str(contract.Id) + 'Group' + str(domainBId)
    groupB[u'GroupRead'] = 1
    groupB[u'GroupWrite'] = 0
    groupB[u'GroupCreate'] = 0
    groupB[u'GroupDelete'] = 0
    groupB[u'GroupDownload'] = 0
    groupB[u'Users'] = groupBUser
    param[u'Groups'] = [groupA, groupB]
    contractAttachment = {}
    if u'uploadFiles' in param:
        for value in param[u'uploadFiles']:
            value[u'Groups'] = [groupA, groupB]
            shareId = shareAttachment(value)
            contractAttachment = ContractAttachment()
            contractAttachment.ContractId = contract.Id
            contractAttachment.ObjectId = value['Id']
            contractAttachment.ShareId = shareId
            contractAttachment.Type = param[u'Type']
            contractAttachment.ProviderUserId = session['UserId']
            db.session.add(contractAttachment)

    return contractAttachment


@moudule.route('/addContractAttachment', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def addContractAttachment():
    session = request.session
    param = request.json_param

    users = ContractUserGroup.query.filter_by(ContractId=param[u'ContractId']).all()
    if u'uploadFiles' not in param:
        return {}

    for value in param[u'uploadFiles']:
        try:
            ContractAttachment.query.filter_by(ContractId=param[u'ContractId'], ObjectId=value[u'Id']).one()
            raise APIException(DataErrorCode.FileAlreadyExist, u'相同附件重复添加')
        except NoResultFound:
            pass
        ca = ContractAttachment()
        ca.ContractId = param[u'ContractId']
        ca.ObjectId = value[u'Id']
        ca.Type = 0
        ca.ProviderUserId = session['UserId']
        ca.Status = 0
        db.session.add(ca)

    c = Contract.query.filter_by(Id=param[u'ContractId']).one()
    log = '制作商\"' + session['CompanyName'] + '\"添加了新的审片素材，请及时查看'
    pm = PlatformMsg('添加审片素材', log, session['UserId'], c.CustomerUserId, c.RequirementId, 'requirement', 'check_attachment')
    db.session.add(pm)
    db.session.commit()
    ca.Id
    return ca


@moudule.route('/getContractAttachment', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def getContractAttachment():
    param = request.json_param
    contractAttachment = db.session.query(ContractAttachment).\
        filter(ContractAttachment.ContractId == param[u'conId']).all()
    return contractAttachment


@moudule.route('/delContractAttachment', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def delContractAttachment():
    param = request.json_param
    if u'AttachmentId' in param:
        attachment = ContractAttachment.query.filter_by(Id=param[u'AttachmentId']).one()
        db.session.delete(attachment)
    db.session.commit()
    return {u'success': True}

@moudule.route('/ContractAttachmentIsPassed', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def ContractAttachmentIsPassed():
    param = request.json_param
    session = request.session
    if u'AttachmentId' in param:
        attachment = ContractAttachment.query.filter_by(Id=param[u'AttachmentId']).one()
        attachment.Status = 1
        log = '用户驳回了审核视频，请及时查看'
        pm = PlatformMsg('驳回审片素材', log, session['UserId'], attachment.ProviderUserId, attachment.Contract.RequirementId, 'requirement', 'check_attachment')
        db.session.add(pm)
    db.session.commit()
    return {u'success': True}

@moudule.route('/ContractAttachmentIsReject', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def ContractAttachmentIsReject():
    param = request.json_param
    session = request.session
    if u'AttachmentId' in param:
        attachment = ContractAttachment.query.filter_by(Id=param[u'AttachmentId']).one()
        attachment.Status = 2
        log = '用户驳回了审核视频，请及时查看'
        pm = PlatformMsg('驳回审片素材', log, session['UserId'], attachment.ProviderUserId, attachment.Contract.RequirementId, 'requirement', 'check_attachment')
        db.session.add(pm)
    db.session.commit()
    return {u'success': True}


@moudule.route('/addMarkPoint', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def addMarkPoint():
    param = request.json_param
    try:
        mark = MarkPoint.query.filter_by(AttachmentId=param[u'AttachmentId'], Time=param[u'Time']).one()
        mark.Content = param[u'Content']
    except NoResultFound:
        mark = MarkPoint(param[u'AttachmentId'], param[u'Time'], param[u'Content'])
        db.session.add(mark)
    db.session.commit()
    return [{'AttachmentId': mark.AttachmentId, 'Time': mark.Time.strftime("%H:%M:%S"), 'Content': mark.Content}]


@moudule.route('/delMarkPoint', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def delMarkPoint():
    param = request.json_param
    try:
        mark = MarkPoint.query.filter_by(AttachmentId=param[u'AttachmentId'], Time=param[u'Time']).one()
    except NoResultFound:
        return param
    db.session.delete(mark)
    db.session.commit()
    return param


@moudule.route('/getMarkPoint', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def getMarkPoint():
    param = request.json_param
    mark = MarkPoint.query.filter(MarkPoint.AttachmentId == param[u'AttachmentId']).order_by(MarkPoint.Time.asc()).all()
    result = []
    for m in mark:
        r = {'AttachmentId': m.AttachmentId, 'Time': m.Time.strftime("%H:%M:%S"), 'Content': m.Content}
        result.append(r)
    return result


@moudule.route('/editContract', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def editContract():
    session = request.session
    param = request.json_param
    contract = Contract.query.filter_by(Id=param[u'Id']).one()
    if contract.Version == 0:
        if contract.Requirement.PublisherId != session['UserId']:
            raise APIException(SystemErrorCode.UnkonwnError, u'需求提交者确认合同后才可修改合同')
        contract.Status = ContractStatus.ContractAppliedNext
        contract.CustomerUserId = contract.Requirement.PublisherId
        contract.Requirement.Status = RequirementStatus.PublishedNext
        conseg = contract.ContractSegment[0]
        conseg.ConfirmUserId = session['UserId']
        conseg.ConfirmTime = datetime.now()
        conseg.ConfirmRemark = u'创建完成'
        conseg.ApplyRemark = u'创建完成'
        conseg.Status = ContractSegmentStatus.Confirmed
        contractseg = ContractSegment()
        contractseg.Remark = u'商订合同'
        contractseg.Deadline = datetime.now()
        contractseg.Segment = ContractSegmentType.Establish
        contractseg.Status = ContractSegmentStatus.Init
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)

        contractseg = ContractSegment()
        contractseg.Remark = u'支付押金'
        contractseg.Deadline = datetime.now()
        contractseg.Segment = ContractSegmentType.Start
        contractseg.Status = ContractSegmentStatus.Init
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)

        contractseg = ContractSegment()
        contractseg.Remark = u'支付尾款'
        contractseg.Deadline = dateutil.parser.parse(param[u'Deadline'])
        contractseg.Segment = ContractSegmentType.Complete
        contractseg.Status = ContractSegmentStatus.Init
        contract.ContractSegmentDynamic.append(contractseg)
        db.session.add(contractseg)
        db.session.flush()
    if contract.Status == ContractStatus.Contracting or contract.Status == ContractStatus.ContractCompleted:
        raise APIException(SystemErrorCode.UnkonwnError, u'合同状态错误，不能修改')
    establishsegment = contract.ContractSegmentDynamic.filter(
        ContractSegment.Segment == ContractSegmentType.Establish).one()
    if establishsegment.Status == ContractSegmentStatus.Applied:
        if session['IsService'] == False:
            if param[u'Returned']:
                establishsegment.Status = ContractSegmentStatus.Returned
            else:
                raise APIException(SystemErrorCode.UnkonwnError, u'合同已申请确认，要修改需先驳回申请')
        else:
            establishsegment.Status = ContractSegmentStatus.Init
        contract.Status = ContractStatus.ContractModifying
    bSaveHistory = False
    if u'Amount' in param:
        test = str(int(contract.Amount))
        if str(int(contract.Amount)) != param[u'Amount']:
            bSaveHistory = True
        contract.Amount = param[u'Amount']
    if u'DepositPercent' in param:
        test = str(int(contract.DepositPercent))
        if str(int(contract.DepositPercent)) != param[u'DepositPercent']:
            bSaveHistory = True
        contract.DepositPercent = param[u'DepositPercent']
    if u'Detail' in param:
        if contract.Detail != param[u'Detail']:
            bSaveHistory = True
        contract.Detail = param[u'Detail']
    if u'Scheme' in param:
        if contract.Scheme != param[u'Scheme']:
            bSaveHistory = True
        contract.Scheme = param[u'Scheme']
    if u'Script' in param:
        if contract.Script != param[u'Script']:
            bSaveHistory = True
        contract.Script = param[u'Script']
    if u'ModifyPerson' in param:
        contract.ModifyPerson = param[u'ModifyPerson']
    endSeg = contract.ContractSegmentDynamic.filter(ContractSegment.Segment == ContractSegmentType.Complete).one()
    endSeg.Deadline = dateutil.parser.parse(param[u'Deadline']).astimezone(tz.tzlocal()).replace(tzinfo=None)
    endSeg = contract.ContractSegmentDynamic.filter(ContractSegment.Segment == ContractSegmentType.End).one()
    endSeg.Deadline = dateutil.parser.parse(param[u'Deadline']).astimezone(tz.tzlocal()).replace(tzinfo=None)
    contract.Version += 1
    reviewSegs = contract.ContractSegmentDynamic.filter(ContractSegment.Segment == ContractSegmentType.Reviewed).all()
    reviewSegs = list(reviewSegs)
    paramSegs = param[u'ContractSegment']
    segDiff = len(paramSegs) - len(reviewSegs)
    contractEventLog = ContractEventLog(contract.Id, session['UserId'], ContractLogActionType.Edit,
                                        ContractSegmentType.Apply , u"修订合同，新版本号" + str(contract.Version))
    db.session.add(contractEventLog)
    if bSaveHistory:
        contractHistory = ContractHistory()
        contractHistory.ContractId = contract.Id
        contractHistory.Version = contract.Version
        contractHistory.ApplyTime = datetime.now()
        contractHistory.ApplyRemark = ""
        contractHistory.Detail = contract.Detail
        contractHistory.ModifyPerson = contract.ModifyPerson
        contractHistory.Scheme = contract.Scheme
        contractHistory.Script = contract.Script
        contractHistory.DepositPercent = contract.DepositPercent
        db.session.add(contractHistory)
    if segDiff > 0:
        for i in range(0, segDiff):
            contractseg = ContractSegment()
            contractseg.Segment = ContractSegmentType.Reviewed
            contractseg.Status = ContractSegmentStatus.Init
            contractseg.ServiceResponser = contract.ServiceUserId
            contractseg.CustomerResponser = contract.CustomerUserId
            contract.ContractSegmentDynamic.append(contractseg)
            contract.ContractSegmentDynamic.append(contractseg)
            db.session.add(contractseg)
            reviewSegs.append(contractseg)
    elif segDiff < 0:
        db.session.execute(
            'delete from contractsegment where contractsegment.ContractId = :contractId and contractsegment.Segment =:SegmentType limit :SegmentCount',
            {
                'contractId': contract.Id,
                'SegmentType': ContractSegmentType.Reviewed, 'SegmentCount': -segDiff})
        reviewSegs = contract.ContractSegmentDynamic.filter(ContractSegment.Segment == ContractSegmentType.Reviewed).all()
    paramSegs = sorted(paramSegs, key=lambda a: dateutil.parser.parse(a[u'Deadline']).astimezone(tz.tzlocal()).replace(
        tzinfo=None))
    for i in range(0, len(paramSegs)):
        reviewSegs[i].Remark = paramSegs[i][u'Remark']
        reviewSegs[i].Deadline = dateutil.parser.parse(paramSegs[i][u'Deadline']).astimezone(tz.tzlocal()).replace(
            tzinfo=None)
    db.session.commit()
    contract.Id
    return contract


@moudule.route('/applyConfirmContract', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def applyConfirmContract():
    session = request.session
    param = request.json_param
    contract = Contract.query.filter_by(Id=param[u'Id']).one()
    if contract.Version != param[u'Version']:
        return APIException(SystemErrorCode.ArgumentError, u'有更新的合同版本存在，请先刷新网页再尝试提交申请!')
    contractSegment = contract.ContractSegmentDynamic.filter(
        ContractSegment.Segment == ContractSegmentType.Establish).one()
    contractSegment.ApplyTime = datetime.now()
    contractSegment.ApplyRemark = param[u'ApplyRemark']
    contractSegment.ApplyUserId = session['UserId']
    contractSegment.Status = ContractSegmentStatus.Applied

    contract.Status = ContractStatus.PayDepositNext
    db.session.commit()
    contract.Id
    return contract


@moudule.route('/getContractHistoryList', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def getContractHistoryList():
    param = request.json_param
    contractHistory = ContractHistory.query.filter_by(ContractId=param[u'ContractId']).all()
    return contractHistory

@moudule.route('/ContractOver', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def ContractOver():
    param = request.json_param
    contract = Contract.query.filter_by(Id=param[u'conId']).one()
    req = Requirement.query.filter_by(Id=param[u'reqId']).one()
    contract.ServiceUser.Domain.Count += contract.Amount
    contract.ServiceUser.Domain.Trade += 1
    req.Status += 1
    db.session.commit()
    return

@moudule.route('/confirmContract', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def confirmContract():
    session = request.session
    param = request.json_param
    contract = Contract.query.filter_by(Id=param[u'Id']).one()
    contractSegment = contract.ContractSegmentDynamic.filter(
        ContractSegment.Id == param[u'SegmentId']).one()

    if param[u'IsReject']:
        contractHistory = db.session.query(ContractHistory).filter(and_(ContractHistory.ContractId == contract.Id, ContractHistory.Version == contract.Version)).one()
        contractHistory.ContractId = contract.Id
        contractHistory.Version = contract.Version
        contractHistory.RejectTime = datetime.now()
        contractHistory.RejectReason = param[u'ConfirmRemark']
        contractHistory.Detail = contract.Detail
        contract.Version += 1
        contractSegment.Status = ContractSegmentStatus.Init

    else:
        contractSegment.ConfirmTime = datetime.now()
        contractSegment.ConfirmRemark = param[u'ConfirmRemark']
        contractSegment.ConfirmUserId = session['UserId']
        contractSegment.Status = ContractSegmentStatus.Confirmed
        contract.Status = ContractStatus.ContractConfirmApplyNext
        if contractSegment.Remark == u'商订合同':
            order = Order(str(uuid4()), '合同押金', '合同押金支付，开启视频制作项目', contract.Amount * contract.DepositPercent / 100, contract.CustomerUserId, contract.ServiceUserId)
            db.session.add(order)
            db.session.flush()
            log = '需求方\'' + contract.CustomerUser.Domain.CompanyName + '\',制作商\'' + \
                  contract.ServiceUser.Domain.CompanyName + '\'的合同：\'' + contract.Title + '\'进入支付押金阶段，押金订单已建立'
            orderLog = OrderLog(order.Id, '合同押金', log, '订单建立')
            db.session.add(orderLog)
            contractOrder = ContractOrder(contract.Id, order.Id, ContractOrderType.PayRent)
            db.session.add(contractOrder)
        elif contractSegment.Remark == u'成片审核':
            order = Order(str(uuid4()), '合同尾款', '合同尾款支付', contract.Amount * (1 - contract.DepositPercent / 100), contract.CustomerUserId, contract.ServiceUserId)
            db.session.add(order)
            db.session.flush()
            log = '需求方\'' + contract.CustomerUser.Domain.CompanyName + '\',制作商\'' + \
                  contract.ServiceUser.Domain.CompanyName + '\'的合同：\'' + contract.Title + '\'进入支付尾款阶段，尾款订单已建立'
            orderLog = OrderLog(order.Id, '合同尾款', log, '订单建立')
            db.session.add(orderLog)
            contractOrder = ContractOrder(contract.Id, order.Id, ContractOrderType.PayRest)
            db.session.add(contractOrder)
        elif contractSegment.Remark == u'交付成片':
            contract.ServiceUser.Domain.Count += contract.Amount


    if param[u'IsReject']:
        title = '环节驳回'
        log = '用户\"' + session['DomainName'] + '\"驳回了您针对合同\"' + contract.Title + '\"的环节确认申请，驳回理由为：\"' + param[u'ConfirmRemark'] + '\"'
    else:
        title = '环节通过'
        log = '用户\"' + session['DomainName'] + '\"通过了您针对合同\"' + contract.Title + '\"的环节确认申请，备注信息为：\"' + param[u'ConfirmRemark'] + '\"'
    contractEventLog = ContractEventLog(contract.Id, session['UserId'],
                                        ContractLogActionType.Deny, ContractSegmentType.Apply, log)
    db.session.add(contractEventLog)
    db.session.flush()
    groupUsers = ContractUserGroup.query.filter_by(ContractId=param[u'Id']).all()
    for u in groupUsers:
        if u.DomainId != session['DomainId']:
            pm = PlatformMsg(title, log, session['UserId'], u.UserId, contract.Requirement.Id, 'contract', 'action')
            db.session.add(pm)

    db.session.commit()
    contract.Id
    return contract


@moudule.route('/payContract', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def payContract():
    session = request.session
    param = request.json_param
    contract = Contract.query.filter_by(Id=param[u'Id']).one()
    contractSegment = contract.ContractSegmentDynamic.filter(ContractSegment.Id == param[u'SegmentId']).one()
    if contractSegment.Status != ContractSegmentStatus.Confirmed:
        contractSegment.ApplyTime = datetime.now()
        contractSegment.ApplyRemark = param[u'ApplyRemark']
        contractSegment.ApplyUserId = session['UserId']
        contractSegment.Status = ContractSegmentStatus.Applied
        if contractSegment.Segment == ContractSegmentType.Start:
            log = u"支付定金"
        elif contractSegment.Segment == ContractSegmentType.Complete:
            log = u"支付尾款"
        contractEventLog = ContractEventLog(contract.Id, session['UserId'],
                                            ContractLogActionType.Apply, ContractSegmentType.Apply, log)
        db.session.add(contractEventLog)
        db.session.commit()
    return contract


@moudule.route('/confirmPayContract', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def confirmPayContract():
    session = request.session
    param = request.json_param
    contract = Contract.query.filter_by(Id=param[u'Id']).one()
    contractSegment = contract.ContractSegmentDynamic.filter(ContractSegment.Id == param[u'SegmentId']).one()
    if contractSegment.Status != ContractSegmentStatus.Confirmed:
        contractSegment.ConfirmTime = datetime.now()
        contractSegment.ConfirmRemark = param[u'ConfirmRemark']
        contractSegment.ConfirmUserId = session['UserId']
        contractSegment.Status = ContractSegmentStatus.Confirmed
        if contractSegment.Segment == ContractSegmentType.Start:
            contract.Status = ContractStatus.PayDepositNext
        elif contractSegment.Segment == ContractSegmentType.Complete:
            contract.Status = ContractStatus.PayAllNext
        db.session.commit()

    # project = Project()
    # project.ContractId = contract.Id
    # project.RequirementId = contract.RequirementId
    # project.PrincipalUserId = session['UserId']
    # for contractseg in contract.ContractSegment:
    # if contractseg.Segment==ContractSegmentType.Reviewed or contractseg.Segment == ContractSegmentType.Complete:
    #         projectseg = ProjectSegment()
    #         projectseg.Deadline = contractSegment.Deadline
    #         projectseg.Remark = contractSegment.Remark
    #         projectseg.Segment = ProjectSegmentType.Reviewed
    #         projectseg.Status = ProjectSegmentStatus.Init
    #         project.ProjectSegmentDynamic.append(projectseg)
    #         db.session.add(projectseg)
    # db.session.add(project)
    return contract


@moudule.route('/applyContractReview', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def applyContractReview():
    session = request.session
    param = request.json_param
    requirement = Requirement.query.filter_by(Id=param[u'reqId']).one()
    requirement.ApplyStatus = 1
    contract = Contract.query.filter_by(Id=param[u'conId']).one()
    user = User.query.filter_by(Id=session['UserId']).one()
    log = '制作商\"' + user.Domain.CompanyName + '\"发起了针对合同\"' + contract.Title + '\"的审核申请确认'
    contractEventLog = ContractEventLog(contract.Id, session['UserId'],
                                        ContractLogActionType.Apply, ContractSegmentType.Reviewed, log)
    db.session.add(contractEventLog)
    db.session.flush()
    groupUsers = ContractUserGroup.query.filter_by(ContractId=contract.Id).all()
    for u in groupUsers:
        if u.DomainId != session['DomainId']:
            pm = PlatformMsg('环节申请', log, session['UserId'], u.UserId, contract.Requirement.Id, 'contract', 'action')
            db.session.add(pm)

    db.session.commit()
    return requirement


@moudule.route('/confirmContractReview', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def confirmContractReview():
    session = request.session
    param = request.json_param
    IsReject = param[u'IsReject']
    requirement = Requirement.query.filter_by(Id=param[u'reqId']).one()
    contract = Contract.query.filter_by(Id=param[u'conId']).one()
    requirement.ApplyStatus = 0
    if IsReject:
        title = '环节驳回'
        log = '用户\"{0}\"驳回了您针对合同\"{1}\"的申请确认行为，理由为：\"{2}\"'.format(session['DomainName'], contract.Title, '环节驳回')
    else:
        requirement.Status += 1
        title = '环节通过'
        log = '用户\"{0}\"通过了您针对合同\"{1}\"的申请确认行为，备注信息：\"{2}\"'.format(session['DomainName'], contract.Title, '环节通过')
        order = Order(str(uuid4()), '合同尾款', '合同尾款支付', contract.Amount * (1 - contract.DepositPercent / 100), contract.CustomerUserId, contract.ServiceUserId)
        db.session.add(order)
        db.session.flush()
        _log = '需求方\'' + contract.CustomerUser.Domain.CompanyName + '\',制作商\'' + contract.ServiceUser.Domain.CompanyName\
               + '\'的合同：\'' + contract.Title + '\'进入支付尾款阶段，尾款订单已建立'
        orderLog = OrderLog(order.Id, '合同尾款', _log, '订单建立')
        db.session.add(orderLog)
        contractOrder = ContractOrder(contract.Id, order.Id, ContractOrderType.PayRest)
        db.session.add(contractOrder)

        ca = db.session.query(ContractAttachment).filter(ContractAttachment.ContractId == contract.Id).all()
        if len(ca) == 0:
            return APIException(SystemErrorCode.ArgumentError, u'没有提交成片')
        else:
            deadline = datetime.datetime.now() + timedelta(days=15)
            for a in ca:
                ap = AttachmentProtect(a.ObjectId, contract.Id, deadline)
                db.session.add(ap)
            db.session.commit()
        # serviceDomain = Domain.query.filter_by(Id=contractSegment.Contract.ServiceUser.DomainId).one()
        # serviceDomain.Trade += 1

    contractEventLog = ContractEventLog(contract.Id, session['UserId'],
                                        ContractLogActionType.Deny, ContractSegmentType.Reviewed, log)
    db.session.add(contractEventLog)
    db.session.flush()
    groupUsers = ContractUserGroup.query.filter_by(ContractId=contract.Id).all()
    for u in groupUsers:
        if u.DomainId != session['DomainId']:
            pm = PlatformMsg(title, log, session['UserId'], u.UserId, contract.Requirement.Id, 'contract', 'action')
            db.session.add(pm)

    db.session.commit()
    return requirement


@moudule.route('/denyPayAll', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def denyPayAll():
    session = request.session
    param = request.json_param
    requirement = Requirement.query.filter_by(Id=param[u'reqId']).one()
    contract = Contract.query.filter_by(Id=param[u'conId']).one()
    requirement.ApplyStatus = 0
    if requirement.Status == RequirementStatus.PayAll:
        requirement.Status = RequirementStatus.Reviewing
    else:
        raise APIException(SystemErrorCode.ArgumentError, u'需求不处于支付尾款环节')

    co = ContractOrder.query.filter_by(ContractId=contract.Id, OrderType=ContractOrderType.PayRest).one()
    order = Order.query.filter_by(Id=co.OrderId).one()
    title = '环节回退'
    log = '用户\"{0}\"反悔了\"{1}\"的支付尾款要求，项目回退到审片环节'.format(session['DomainName'], contract.Title)
    _log = '需求方\'' + contract.CustomerUser.Domain.CompanyName + '\',制作商\'' + contract.ServiceUser.Domain.CompanyName\
           + '\'的合同：\'' + contract.Title + '\'，用户反悔，环节回退到审片'
    orderLog = OrderLog(order.Id, '合同尾款', _log, '用户反悔')
    contractEventLog = ContractEventLog(contract.Id, session['UserId'], ContractLogActionType.Deny,
                                        ContractSegmentType.Reviewed, log)
    db.session.add(orderLog)
    db.session.add(contractEventLog)

    db.session.delete(co)
    db.session.delete(order)
    AttachmentProtect.query.filter_by(ContractId=contract.Id).delete()
    groupUsers = ContractUserGroup.query.filter_by(ContractId=contract.Id).all()
    for u in groupUsers:
        if u.DomainId != session['DomainId']:
            pm = PlatformMsg(title, log, session['UserId'], u.UserId, contract.Requirement.Id, 'contract', 'action')
            db.session.add(pm)
    db.session.commit()
    return {}


@moudule.route('/getContractSegmentLog', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def getContractSegmentLog():
    param = request.json_param
    log = ContractSegmentLog.query.filter_by(ContractId=param[u'ContractId'], SegmentId=param[u'SegmentId']).all()
    return log


@moudule.route('/createProject', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def createProject():
    session = request.session
    param = request.json_param
    contractId = None
    try:
        contractId = param[u'ContractId']
    except KeyError:
        pass
    if not session['IsService']:
        return APIException(SystemErrorCode.ArgumentError, u'只有服务商可以创建工程')
    if contractId is not None and Project.query.filter_by(ContractId=contractId).count() >= 1:
        return APIException(SystemErrorCode.ArgumentError, u"该合同对应项目已存在，不能重复创建项目")
    project = Project()
    project.Title = param[u'Title']
    project.Detail = param[u'Detail']
    project.PrincipalUserId = param[u'PrincipalUserId']
    project.ContractId = contractId
    if contractId is not None:
        project.RequirementId = Contract.query.filter_by(Id=project.ContractId).one().RequirementId
    db.session.add(project)
    for s in param[u'Segments']:
        projectSegment = ProjectSegment()
        try:
            projectSegment.ContractSegmentId = s[u'ContractSegmentId']
        except KeyError:
            pass
        projectSegment.PrincipalUserId = s[u'PrincipalUserId']
        projectSegment.Remark = s[u'Remark']
        projectSegment.Deadline = dateutil.parser.parse(s[u'Deadline'])
        projectSegment.Segment = s[u'Segment']
        projectSegment.Status = ProjectSegmentStatus.Init
        project.ProjectSegmentDynamic.append(projectSegment)
        db.session.add(projectSegment)
    projectEventLog = ProjectEventLog()
    project.ProjectEventLog.append(projectEventLog)
    projectEventLog.UserId = session['UserId']
    projectEventLog.Segment = projectSegment.Segment
    projectEventLog.Detail = u"创建项目"
    db.session.add(projectEventLog)
    db.session.commit()
    project.Id
    return project


@moudule.route('/project', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def project():
    session = request.session
    param = request.json_param
    project = db.session.query(Project).filter(Project.PrincipalUserId == session['UserId'])
    if u'Id' in param:
        project = project.filter_by(Id=param[u'Id'])
    return project.all()

@moudule.route('/downloadAttachment/<string:code>', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def downloadAttachment(code):
    session = request.session
    param = request.json_param
    userId = session['UserId']
    code = base64.decodestring(code)
    codeType = code[1]
    code = code[1:]
    code = code.split(',')
    for i in range(0,len(code)):
        code[i]=int(code[i],16)
    OwnerId = code[0]
    ProjectId = code[1]
    ObjectId = code[2]
    project = Project.query.filter_by(Id = ProjectId).one()
    contract = project.Contract
    if not(contract.CustomerUserId == userId or project.PrincipalUserId == userId):
        return  APIException(SystemErrorCode.DataError,u'非环节相关负责人不允许下载')
    obj = Object.query.filter_by(Id=ObjectId, OwnerUserId=OwnerId).one()
    if obj.File is None:
        return APIException(40400, u'非文件对象不能下载')

    from Main import app
    resp = app.make_response((''))
    resp.headers['X-Accel-Redirect'] = '/' + os.path.join(G_UPLOAD_FILE_FLODER_REL, obj.File.Path)
    resp.headers['Content-Type'] = ''
    resp.headers['Content-Disposition'] = ('attachment; filename=' + obj.Name).encode('utf8')
    return resp


@moudule.route('/applyProjectSegment', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def applyProjectSegment():
    session = request.session
    param = request.json_param
    projectSegment = ProjectSegment.query.filter_by(Id=param[u'SegmentId']).one()
    if not (projectSegment.PrincipalUserId == session['UserId'] or projectSegment.Project.PrincipalUserId == session[
        'UserId']):
        raise APIException(SystemErrorCode.DataError,u'无权限申请项目流程')

    contractId = projectSegment.Project.ContractId
    attachments = []
    if contractId is not None and u'Attachments' in param:
        for a in param[u'Attachments']:
            #a[u'ContractId'] = contractId
            OwnerId = sharedPermissionValidate(Permission.PermissionShare, param=a)
            ProjectId = projectSegment.ProjectId
            ObjectId = a['Id']
            Name = a[u'Name']
            code = 'P'+hex(OwnerId)[2:]+','+hex(ProjectId)[2:]+','+hex(ObjectId)[2:]
            encodedCode = base64.encodestring(code)
            attachments.append({'Name':Name,'DownloadCode':encodedCode})
    ApplyRemark = JSONEncoder(ensure_ascii=False).encode({'Remark':param[u'ApplyRemark'],'Attachments':attachments})
    projectSegment.ApplyTime = datetime.now()
    projectSegment.ApplyRemark = ApplyRemark
    projectSegment.ApplyUserId = session['UserId']
    projectSegment.Status = ProjectSegmentStatus.Applied
    if projectSegment.ContractSegment:
        projectSegment.ContractSegment.ApplyTime = datetime.now()
        projectSegment.ContractSegment.ApplyRemark = projectSegment.ApplyRemark
        projectSegment.ContractSegment.ApplyUserId = projectSegment.ApplyUserId
        projectSegment.ContractSegment.Status = ContractSegmentStatus.Applied
    projectEventLog = ProjectEventLog()
    projectEventLog.ProjectId = projectSegment.ProjectId
    projectEventLog.UserId = session['UserId']
    projectEventLog.Segment = projectSegment.Segment
    projectEventLog.Detail = u"申请" + projectSegment.Remark
    db.session.add(projectEventLog)
    db.session.commit()
    return Project.query.filter_by(Id=projectSegment.ProjectId).one()


@moudule.route('/confirmProjectSegment', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def confirmProjectSegment():
    session = request.session
    param = request.json_param
    IsReject = param[u'IsReject']
    if IsReject:
        logStr = u'确认'
    else:
        logStr = u'拒绝'
    projectSegment = ProjectSegment.query.filter_by(Id=param[u'SegmentId']).one()
    if projectSegment.Project.Contract is not None and not (
        projectSegment.Project.Contract.ServiceUserId == session['UserId']):
        raise APIException(SystemErrorCode.DataError, u'无权限确认项目流程')
    projectSegment.ConfirmTime = datetime.now()
    projectSegment.ConfirmRemark = param[u'ConfirmRemark']
    projectSegment.ConfirmUserId = session['UserId']
    if IsReject:
        projectSegment.Status = ProjectSegmentStatus.Returned
    else:
        projectSegment.Status = ProjectSegmentStatus.Confirmed
    if projectSegment.ContractSegment:
        if IsReject:
            projectSegment.ContractSegment.ApplyUserId = None
            projectSegment.ContractSegment.ApplyRemark = None
            projectSegment.ContractSegment.ApplyTime = None
            projectSegment.ContractSegment.ConfirmUserId = None
            projectSegment.ContractSegment.ConfirmRemark = None
            projectSegment.ContractSegment.ConfirmTime = None
            projectSegment.ContractSegment.Status = ContractSegmentStatus.Init
        else:
            raise APIException(SystemErrorCode.DataError, u'无权限确认项目流程,确认只能由用户发起')
    projectEventLog = ProjectEventLog()
    projectEventLog.ProjectId = projectSegment.ProjectId
    projectEventLog.UserId = session['UserId']
    projectEventLog.Segment = projectSegment.Segment
    projectEventLog.Detail = logStr + projectSegment.Remark
    db.session.add(projectEventLog)
    db.session.commit()
    return Project.query.filter_by(Id=projectSegment.ProjectId).one()


@moudule.route('/getScheme', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getScheme():
    param = request.json_param
    try:
        scheme = Scheme.query.filter_by(ContractId=param[u'ContractId']).one()
    except NoResultFound:
        scheme = Scheme(1, param[u'ContractId'])
        db.session.add(scheme)
        db.session.flush()
        db.session.commit()
        scheme.Id
    scheme.SchemeHistory
    return scheme


@moudule.route('/saveScheme', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveScheme():
    param = request.json_param
    scheme = Scheme.query.filter_by(Id=param[u'Id']).one()
    if scheme.Version != param[u'Version']:
        return APIException(SystemErrorCode.UnkonwnError, u'版本不一致，请重新修改')

    scheme.Version += 1
    scheme.Detail = param[u'Detail']
    db.session.commit()
    scheme.Id
    return scheme


@moudule.route('/getScript', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getScript():
    param = request.json_param
    try:
        script = Script.query.filter_by(ContractId=param[u'ContractId']).one()
    except NoResultFound:
        script = Script(1, param[u'ContractId'])
        db.session.add(script)
        db.session.flush()
        db.session.commit()
        script.Id
    script.ScriptHistory
    return script


@moudule.route('/saveScript', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveScript():
    param = request.json_param
    script = Script.query.filter_by(Id=param[u'Id']).one()
    if script.Version != param[u'Version']:
        return APIException(SystemErrorCode.UnkonwnError, u'版本不一致，请重新修改')

    script.Version += 1
    script.Detail = param[u'Detail']
    db.session.commit()
    script.Id
    return script


@moudule.route('/getContractClips', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getContractClips():
    param = request.json_param
    try:
        contractClips = ContractClips.query.filter_by(ContractId=param[u'ContractId']).one()
    except NoResultFound:
        contractClips = ContractClips(1, param[u'ContractId'])
        db.session.add(contractClips)
        db.session.flush()
        db.session.commit()
        contractClips.Id
    contractClips.ContractClipsHistory
    return contractClips


@moudule.route('/saveContractClips', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveContractClips():
    param = request.json_param
    contractClips = ContractClips.query.filter_by(Id=param[u'Id']).one()
    if contractClips.Version != param[u'Version']:
        return APIException(SystemErrorCode.UnkonwnError, u'版本不一致，请重新修改')

    contractClips.Version += 1
    contractClips.Detail = param[u'Detail']

    db.session.commit()
    contractClips.Id
    return contractClips


@moudule.route('/getReviewVideo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getReviewVideo():
    param = request.json_param
    try:
        reviewVideo = ReviewVideo.query.filter_by(ContractId=param[u'ContractId']).one()
    except NoResultFound:
        reviewVideo = ReviewVideo(1, param[u'ContractId'])
        db.session.add(reviewVideo)
        db.session.flush()
        db.session.commit()
        reviewVideo.Id
    reviewVideo.ReviewVideoHistory
    return reviewVideo


@moudule.route('/saveReviewVideo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveReviewVideo():
    param = request.json_param
    reviewVideo = ReviewVideo.query.filter_by(Id=param[u'Id']).one()
    if reviewVideo.Version != param[u'Version']:
        return APIException(SystemErrorCode.UnkonwnError, u'版本不一致，请重新修改')

    reviewVideo.Version += 1
    reviewVideo.Detail = param[u'Detail']
    db.session.commit()
    reviewVideo.Id
    return reviewVideo


@moudule.route('/getFinalVideo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getFinalVideo():
    param = request.json_param
    try:
        finalVideo = FinalVideo.query.filter_by(ContractId=param[u'ContractId']).one()
    except NoResultFound:
        finalVideo = FinalVideo(1, param[u'ContractId'])
        db.session.add(finalVideo)
        db.session.flush()
        db.session.commit()
        finalVideo.Id
    finalVideo.FinalVideoHistory
    return finalVideo


@moudule.route('/saveFinalVideo', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def saveFinalVideo():
    param = request.json_param
    finalVideo = FinalVideo.query.filter_by(Id=param[u'Id']).one()
    if finalVideo.Version != param[u'Version']:
        return APIException(SystemErrorCode.UnkonwnError, u'版本不一致，请重新修改')

    finalVideo.Version += 1
    finalVideo.Detail = param[u'Detail']
    db.session.commit()
    finalVideo.Id
    return finalVideo


@moudule.route('/aliPay', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def aliPay():
    param = request.json_param
    session = request.session
    order = Order.query.filter_by(Id=param[u'OrderId']).one()
    user = User.query.filter_by(Id=session['UserId']).one()
    # 使用平台账号余额支付
    useAccount = round_(float(param[u'UseAccount']))
    if useAccount > 0:
        # 余额充足
        if user.Domain.Count >= useAccount:
            order.UseAccount = useAccount
        else:
            return {'bSuccess': False, 'description': '您的平台账号余额不足!'}
    db.session.commit()
    # 订单完全使用余额支付，直接完成
    if order.Amount - order.UseAccount <= 0:
        pay_notify(order.SerialNumber, 'TRADE_SUCCESS')
        return {'bSuccess': True, 'bAlipay': False}
    else:
        url = create_direct_pay_by_user(order.SerialNumber, param['Subject'], param['Description'], order.Amount - order.UseAccount)
        #去支付页面
        return {'bSuccess': True, 'bAlipay': True, 'description': url}


@moudule.route('/aliPay_notify', methods=['GET', 'POST'])
@output_data
def aliPay_notify():
    print "aliPay_notify"
    param = request.json_param
    for i in param:
        print "dict[%s]=" % i, param[i]
    orderId = param[u'out_trade_no']
    tradeStatus = param[u'trade_status']
    return pay_notify(orderId, tradeStatus)


def pay_notify(orderId, tradeStatus):
    order = Order.query.filter_by(SerialNumber=orderId).one()

    if tradeStatus == 'TRADE_SUCCESS':
        order.State = OrderState.Payed

        user = User.query.filter_by(Id=order.PayUserId).one()
        user.Domain.Count -= order.UseAccount

        try: #购买扩展存储空间
            eo = ExtendStorageOrder.query.filter_by(OrderId=order.Id).one()
            user.Domain.ExtendStorageSize += eo.ExtendStorageSize * 1024 * 1024 * 1024
            if user.Domain.ESExpireTime is None:
                user.Domain.ESExpireTime = datetime.now()
            user.Domain.ESExpireTime = user.Domain.ESExpireTime + timedelta(days=eo.ExtendTime * 31)
            log = '用户\'' + user.Domain.CompanyName + '\'购买额外存储空间的订单完成支付，空间已扩展'
            orderLog = OrderLog(order.Id, '购买存储空间', log, '订单支付完成')
            db.session.add(orderLog)
        except NoResultFound:
            pass

        try: #平台账号充值
            rao = RechargeAccountOrder.query.filter_by(OrderId=order.Id).one()
            user.Domain.Count += rao.Amount
            log = '用户\'' + user.Domain.CompanyName + '\'为平台账号充值的订单完成支付，账号已充值'
            orderLog = OrderLog(order.Id, '平台账号充值', log, '订单支付完成')
            db.session.add(orderLog)
            zi = ZoneItem.query.filter_by(DomainId=user.DomainId).all()
            for v in zi:
                v.Weight = 1
            user.Domain.Weight = 1
        except NoResultFound:
            pass

        try: #合同押金支付
            co = ContractOrder.query.filter_by(OrderId=order.Id).one()
            contract = Contract.query.filter_by(Id=co.ContractId).one()
            requirement = Requirement.query.filter_by(ContractId=contract.Id).one()

            if requirement.Status == RequirementStatus.PayDeposit:
                requirement.Status = RequirementStatus.Reviewing
                orderType = '合同押金'
            elif requirement.Status == RequirementStatus.PayAll:
                requirement.Status = RequirementStatus.Retainage
                orderType = '合同尾款'
            log = '需求方\'' + order.PayUser.Domain.CompanyName + '\',制作商\'' + order.Receiver.Domain.CompanyName + \
                  '\'的合同(' + contract.Title + '),' + orderType + '支付完成，费用已转给商影联盟'
            orderLog = OrderLog(order.Id, orderType, log, '订单支付完成')
            db.session.add(orderLog)
        except NoResultFound:
            pass

        try: #会员会费支付
            mso = MemberShipTaxOrder.query.filter_by(OrderId=order.Id).one()
            user.Domain.ExpireTime = mso.ExpireTime
            log = '用户\'' + user.Domain.CompanyName + '\'的会员会费订单完成支付'
            orderLog = OrderLog(order.Id, '会员会费', log, '订单支付完成')
            db.session.add(orderLog)
        except NoResultFound:
            pass

        db.session.commit()
    else:
        order.State = OrderState.UnPay

        try: #购买扩展存储空间
            ExtendStorageOrder.query.filter_by(OrderId=order.Id).one()
            user = User.query.filter_by(Id=order.PayUserId).one()
            log = '用户\'' + user.Domain.CompanyName + '\'购买额外存储空间的订单支付失败，支付宝回复的状态码为：' + tradeStatus
            orderLog = OrderLog(order.Id, '购买存储空间', log, '订单支付失败')
            db.session.add(orderLog)
        except NoResultFound:
            pass

        try: #平台账号充值
            RechargeAccountOrder.query.filter_by(OrderId=order.Id).one()
            user = User.query.filter_by(Id=order.PayUserId).one()
            log = '用户\'' + user.Domain.CompanyName + '\'为平台账号充值的订单支付失败，支付宝回复的状态码为：' + tradeStatus
            orderLog = OrderLog(order.Id, '平台账号充值', log, '订单支付失败')
            db.session.add(orderLog)
        except NoResultFound:
            pass

        try: #合同押金支付
            co = ContractOrder.query.filter_by(OrderId=order.Id).one()
            contract = Contract.query.filter_by(Id=co.ContractId).one()
            orderType = '合同押金'
            if co.OrderType == ContractOrderType.PayRest:
                orderType = '合同尾款'
            log = '需求方\'' + order.PayUser.Domain.CompanyName + '\',制作商\'' + order.Receiver.Domain.CompanyName + \
                  '\'的合同(' + contract.Title + '),' + orderType + '支付失败，支付宝回复的状态码为：' + tradeStatus
            orderLog = OrderLog(order.Id, orderType, log, '订单支付失败')
            db.session.add(orderLog)
        except NoResultFound:
            pass

        try: #会员会费支付
            MemberShipTaxOrder.query.filter_by(OrderId=order.Id).one()
            user = User.query.filter_by(Id=order.PayUserId).one()
            log = '用户\'' + user.Domain.CompanyName + '\'的会员会费订单支付失败，支付宝回复的状态码为：' + tradeStatus
            orderLog = OrderLog(order.Id, '会员会费', log, '订单支付失败')
            db.session.add(orderLog)
        except NoResultFound:
            pass

        db.session.commit()

    return {}


@moudule.route('/contractOrder', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def contractOrder():
    param = request.json_param
    co = ContractOrder.query.filter_by(ContractId=param[u'ContractId'], OrderType=param[u'OrderType']).one()
    return co.Order

@moudule.route('/getAllOrder', methods=['GET', 'POST'])
@PermissionValidate()
@output_data
def getAllOrder():
    param = request.json_param
    order = ContractOrder.query.all()
    return order


@moudule.route('/CreateOrder', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def CreateOrder():
    param = request.json_param
    session = request.session
    order_type = param[u'OrderType']
    #平台账号充值
    if order_type == 'RechargeAccount':
        order = Order(str(uuid4()), '充值', '充值:'+str(param[u'RechargeAccount']), float(param[u'RechargeAccount']), session['UserId'], '0')
        db.session.add(order)
        db.session.flush()
        log = '用户\'' + session['CompanyName'] + '\'选择为平台账号充值，充值订单已建立'
        orderLog = OrderLog(order.Id, '平台账号充值', log, '订单建立')
        db.session.add(orderLog)
        eo = RechargeAccountOrder(float(param[u'RechargeAccount']), order.Id)
        db.session.add(eo)
    #购买额外的存储空间
    elif order_type == 'ExtendStorage':
        price = float(param[u'Price'])
        useCount = float(param[u'UseCount'])
        if price > 0:
            order = Order(str(uuid4()), '增值服务', '使用平台余额:'+str(useCount), price, session['UserId'], '0')
            db.session.add(order)
            db.session.flush()
            log = '用户\'' + session['CompanyName'] + '\'选择购买额外的存储空间，购买订单已建立'
            orderLog = OrderLog(order.Id, '购买存储空间', log, '订单建立')
            db.session.add(orderLog)
            eo = ExtendStorageOrder(param[u'ExtendTime'], useCount, param[u'ExtendStorage'], order.Id)
            db.session.add(eo)
    #会员续费
    elif order_type == 'MemberShipTax':
        domain = Domain.query.filter_by(Id=session['DomainId']).one()
        year = int(param[u'Year'])
        cur_time = datetime.now()
        if domain.ExpireTime > cur_time:
            original_expire_time = domain.ExpireTime
        else:
            original_expire_time = cur_time
        ps = PlatformSetting.query.one()
        price = year * ps.MemberShipTax
        order = Order(str(uuid4()), '会员续费服务', '使用平台余额:0', price, session['UserId'], '0')
        db.session.add(order)
        db.session.flush()
        log = '用户\'' + session['CompanyName'] + '\'选择进行会员续费，续费订单已建立'
        orderLog = OrderLog(order.Id, '会员续费', log, '订单建立')
        db.session.add(orderLog)
        mso = MemberShipTaxOrder(original_expire_time, original_expire_time + timedelta(days=365*year), order.Id)
        db.session.add(mso)

    db.session.commit()
    order.Id
    return order

@moudule.route('/videoCategory', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def videoCategory():
    param = request.json_param
    if u'ParentId' in param:
        category = Category.query.filter_by(ParentId=param[u'ParentId']).all()
    else:
        category = Category.query.filter_by(Level=1).all()
    return category


@moudule.route('/getReqTemplate', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def getReqTemplate():
    param = request.json_param
    try:
        return RequirementTemplate.query.filter_by(Category_1=param[u'Category_1'], Category_2=param[u'Category_2']).one()
    except NoResultFound:
        return APIException(SystemErrorCode.UnkonwnError, u'无此类模板')


@moudule.route('/platformSetting', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def platformSetting():
    return PlatformSetting.query.one()


@moudule.route('/moneySetting', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def moneySetting():
    d = Domain.query.filter().order_by(Domain.Price.desc()).limit(10).all()
    price = d[len(d) - 1].Price
    return {'setting': PlatformSetting.query.one(), 'domainPrice': price}

import time

@moudule.route('/longQuery', methods=['POST'])
@output_data
@PermissionValidate()
def longQuery():
    session = request.session
    # timeout = 10
    # step = 0
    # while step < timeout:
    #     pm = PlatformMsg.query.filter_by(DestUserId=session['UserId'], IsAdopted=0).all()
    #     if len(pm) > 0:
    #         for v in pm:
    #             v.IsAdopted = 1
    #         db.session.commit()
    #         return {'status': 'newMsg'}
    #     time.sleep(5)
    #     step += 5
    # return {'status': 'timeout'}
    pm = PlatformMsg.query.filter_by(DestUserId=session['UserId'], IsAdopted=0).all()
    if len(pm) > 0:
        lastMsg = pm[0].Msg
        for v in pm:
            v.IsAdopted = 1
        db.session.commit()
        return {'status': 'newMsg', 'latestMsg': lastMsg}
    return {'status': 'timeout'}


@moudule.route('/getMsg', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def getMsg():
    session = request.session
    pm = db.session.query(PlatformMsg).filter(PlatformMsg.DestUserId == session['UserId'])\
        .order_by(PlatformMsg.CreateTime.desc()).all()
    result = []
    for v in pm:
        result.append({'Id': v.Id, 'Title': v.Title, 'Msg': v.Msg, 'SrcUserId': v.SrcUserId,
                       'DestUserId': v.DestUserId, 'ResourceId': v.ResourceId, 'ResourceType': v.ResourceType,
                       'MsgType': v.MsgType, 'IsReaded': v.IsReaded, 'IsAdopted': v.IsAdopted,
                       'CreateTime': v.CreateTime})
        v.IsReaded = 1
    db.session.commit()
    return result


@moudule.route('/delMsg', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def delMsg():
    param = request.json_param
    session = request.session
    if u'UserId' in param:
        PlatformMsg.query.filter_by(DestUserId=param[u'UserId']).delete()
    elif u'MsgId' in param:
        PlatformMsg.query.filter_by(Id=param[u'MsgId']).delete()
    elif u'RequirementId' in param:
        PlatformMsg.query.filter_by(DestUserId=session['UserId'], ResourceId=param[u'RequirementId'], ResourceType='requirement').delete()
    db.session.commit()
    return {}


@moudule.route('/modifyDomainPrice', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def modifyDomainPrice():
    param = request.json_param
    session = request.session
    d = Domain.query.filter_by(Id=session['DomainId']).one()
    d.Price = param[u'Price']
    if d.Count > d.Price:
        d.Weight = 1
    else:
        d.Weight = 0
    db.session.commit()
    return {}


@moudule.route('/loginImage', methods=['POST'])
@output_data
def loginImage():
    path = db.session.query(Settings).filter(Settings.Item == 'LoginImage').one().Value
    return path


@moudule.route('/applyAbortContract', methods=['POST'])
@PermissionValidate()
@output_data
def applyAbortContract():
    param = request.json_param
    session = request.session
    try:
        car = ContractAbortRecord.query.filter_by(ContractId=param[u'ContractId']).one()
        c = Contract.query.filter_by(Id=param[u'ContractId']).one()
        if c.Status == ContractStatus.Last:
            return {'bSuccess': False}
        car.Status = 'apply'
        car.ApplyRemark = param[u'ApplyRemark']
        c.Procedure = 'applyAbort'
        db.session.commit()
        return {'bSuccess': True}
    except NoResultFound:
        car = ContractAbortRecord(param[u'ContractId'], param[u'ApplyRemark'], session['UserId'], session['DomainId'], datetime.now())
        c = Contract.query.filter_by(Id=param[u'ContractId']).one()
        if c.Status == ContractStatus.Last:
            return {'bSuccess': False}
        c.Procedure = 'applyAbort'
        db.session.add(car)
        db.session.commit()
        return {'bSuccess': True}


@moudule.route('/getContractAbortStatus', methods=['POST'])
@PermissionValidate()
@output_data
def getContractAbortStatus():
    param = request.json_param
    try:
        car = ContractAbortRecord.query.filter_by(ContractId=param[u'ContractId']).one()
        return car
    except NoResultFound:
        return {}


@moudule.route('/addFollowerAttachment', methods=['POST'])
@PermissionValidate()
@output_data
def addFollowerAttachment():
    param = request.json_param
    for v in param[u'Files']:
        fa = FollowerAttachment(param[u'FollowerId'], v[u'Id'])
        db.session.add(fa)
    db.session.commit()
    fas = FollowerAttachment.query.filter_by(FollowerId=param[u'FollowerId']).all()
    return fas


@moudule.route('/delFollowerAttachment', methods=['POST'])
@PermissionValidate()
@output_data
def delFollowerAttachment():
    param = request.json_param
    fa = FollowerAttachment.query.filter_by(Id=param[u'AttachmentId']).one()
    faId = fa.FollowerId
    db.session.delete(fa)
    db.session.flush()
    db.session.commit()
    fas = FollowerAttachment.query.filter_by(FollowerId=faId).all()
    return fas


@moudule.route('/applyMoney', methods=['GET', 'POST'])
@output_data
@PermissionValidate()
def applyMoney():
    param = request.json_param
    session = request.session
    try:
        ApplyMoney.query.filter_by(UserId=session['UserId'], Status=ApplyMoneyStatus.applying).one()
        return {u'您已经有正在申请的提现'}
    except NoResultFound:
        domain = Domain.query.filter_by(Id=session['DomainId']).one()
        if domain.Count >= float(param[u'account']):
            domain.Count -= float(param[u'account'])
        else:
            raise APIException(SystemErrorCode.UnkonwnError, u'提现金额大于账号金额！')
        am = ApplyMoney(session['DomainId'], session['UserId'], param[u'account'])
        db.session.add(am)
        db.session.commit()
    return {}


@moudule.route('/leaveMsg', methods=['GET', 'POST'])
@output_data
def leaveMsg():
    param = request.json_param
    lm = LeaveMsg(param[u'msg'], param[u'name'], param[u'phone'], param[u'email'])
    db.session.add(lm)
    db.session.commit()
    return {}