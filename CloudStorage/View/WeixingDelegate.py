# -*- coding: utf-8 -*-
__author__ = 'huiteng'

from flask import request, redirect, render_template, Blueprint, session, flash
from flask.views import MethodView
from Tools.DataPaser import incoming_params, output_data,output_data_without_attribute, expandAttribute, jsonDecoder
from Models.CloudStorge import *
from Models.Platform import *
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_
from functools import wraps
from Tools.APIException import *
from Tools import MailSender
from urllib import quote
from datetime import timedelta,datetime
from Tools.DataPaser import output_data, output_data_without_attribute, expandAttribute, round_

import urllib2
import time
import random
import string
import hashlib
from Tools.Permision import PermissionValidate, sharedPermissionValidate, Permission, objectOperatePermission

weixing = Blueprint('weixing', __name__, template_folder='templates', static_folder='static')
restfulApi = None

APPID = 'wx7d438d00f2f8e9ec'
SECRET = '211cc4dcb2efe22611c3c18e059292d6'

#微信提供的API接口，除URL_CREATE_MENU创建菜单外，其余均是鉴权
URL_ACCESSTOKEN = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(APPID, SECRET)
URL_GETUSERTOKEN = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'
URL_OAUTH = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base&state=1#wechat_redirect'
URL_GETJSTICKET = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi'
URL_GETUSERINFO = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang=zh_CN'
URL_CREATE_MENU = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='

def route_config(app, api):
    app.register_blueprint(weixing, url_prefix='/mobile')
    global restfulApi
    restfulApi = api

#############权限相关函数#########################################
def check_user_inner():
    if 'UserId' not in session:
        try:
            incoming = request.json_param
            #session['openId'] = 'opW19wWbghHEclmiY7CsGpj53hYE' #for 测试

            if u'code' in incoming and 'openId' not in session:
                weixinCode = incoming[u'code']

                result = urllib2.urlopen(URL_GETUSERTOKEN.format(APPID, SECRET, weixinCode)).read()
                result = jsonDecoder.decode(result)

                if u'openid' in result:
                    session['openId'] = result[u'openid']

            if  'openId' in session:
                user = User.query.filter_by(WeiXinOpenId=session['openId']).one()
                session['UserId'] = user.Id
        except:
            pass

def check_user(resource):
    @wraps(resource)
    def wrapper(*args, **kwargs):
        check_user_inner()
        return resource(*args, **kwargs)
    return wrapper

def check_login(resource):
    @wraps(resource)
    def wrapper(*args, **kwargs):
        check_user_inner()
        if 'UserId' not in session:
            return restfulApi.make_response({'bSuccess': False, 'error':'未登录', 'Path': 'http://jianpianzi.com/mobile/bindWX?path=' + request.path}, 200, headers='')
        return resource(*args, **kwargs)
    return wrapper

def check_login2(resource):
    @wraps(resource)
    def wrapper(*args, **kwargs):
        check_user_inner()
        if 'UserId' not in session:
            return render_template('mobile/bindWX.html', path=request.path)
        return resource(*args, **kwargs)
    return wrapper

#############微信js票据相关#########################################
class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

def weixin_refresh(resource):
    @wraps(resource)
    def wrapper(*args, **kwargs):
        bRefresh = False

        # 查看accessToken是否要刷新
        token = db.session.query(WeiXinToken).first()
        if token:
            duration = datetime.now() - token.CreateTime
            if duration > timedelta(seconds=token.Expires_in):
                bRefresh = True
        else:
            bRefresh = True

        # 查看jsapiTicket是否要刷新
        ticket = db.session.query(WeiXinJsTicket).first()
        if ticket:
            duration = datetime.now() - ticket.CreateTime
            if duration > timedelta(seconds=ticket.Expires_in):
                bRefresh = True
        else:
            bRefresh = True

        if bRefresh:
            result = urllib2.urlopen(URL_ACCESSTOKEN).read()
            result = jsonDecoder.decode(result)

            if 'access_token' in result:
                access_token = result['access_token']

                if token:
                    token.AccessToken = access_token
                    token.Expires_in = result['expires_in']
                    token.CreateTime = datetime.now()
                else:
                    wxToken = WeiXinToken(access_token, result['expires_in'])
                    db.session.add(wxToken)

                r = urllib2.urlopen(URL_GETJSTICKET.format(access_token)).read()
                r = jsonDecoder.decode(r)

                if r['errcode'] == 0:
                    js_ticket = r['ticket']

                    if ticket:
                        ticket.JsapiTicket = js_ticket
                        ticket.Expires_in = r['expires_in']
                        ticket.CreateTime = datetime.now()
                    else:
                        wxTicket = WeiXinJsTicket(js_ticket, r['expires_in'])
                        db.session.add(wxTicket)
                else:
                    return resource(*args, **kwargs) #restfulApi.make_response({'bSuccess': False, 'error': u'get jsTicket failed'}, 200, headers='')

                db.session.commit()
            elif 'errmsg' in result:
                return resource(*args, **kwargs) #restfulApi.make_response({'bSuccess': False, 'error': r['errmsg']}, 200, headers='')
            else:
                return resource(*args, **kwargs) #restfulApi.make_response({'bSuccess': False, 'error': u'network error'}, 200, headers='')
        else:
            access_token = token.AccessToken
            js_ticket = ticket.JsapiTicket

        request.accessToken = access_token
        request.jsTicket = js_ticket

        sign = Sign(js_ticket, request.url)
        print sign.sign()

        request.signature = sign.ret['signature']
        request.nonceStr = sign.ret['nonceStr']
        request.timestamp = sign.ret['timestamp']

        return resource(*args, **kwargs)
    return wrapper

#############微信操作相关#########################################
# 配置微信菜单
@weixing.route('/weixinSetting', methods=['GET'])
@incoming_params
def weixinSetting():
    result = urllib2.urlopen(URL_ACCESSTOKEN).read()
    result = jsonDecoder.decode(result)

    if 'access_token' in result:
        access_token = result['access_token']
        url = URL_CREATE_MENU + access_token
        print access_token
        values = {"button": [{"type": "view",
                              "name": "案例推荐",
                              "url": URL_OAUTH.format(APPID, quote('http://jianpianzi.com/mobile/promote'))},
                             {"type": "view",
                              "name": "制作管理",
                               "url": URL_OAUTH.format(APPID, quote('http://jianpianzi.com/mobile/submit'))},
                             {"name": "我的空间",
                              "sub_button": [{"type": "view",
                                              "name": "我的视频",
                                              "url": URL_OAUTH.format(APPID, quote('http://jianpianzi.com/mobile/media'))},
                                             # {"type": "view",
                                             #  "name": "查看帮助",
                                             #  "url": URL_OAUTH.format(APPID, quote('http://jianpianzi.com/mobile/help'))},
                                             {"type": "view",
                                              "name": "牵手联盟",
                                              "url": URL_OAUTH.format(APPID, quote('http://jianpianzi.com/mobile/aboutus'))}, # 增加注销功能
                                             # {"type": "view",
                                             #  "name": "注销",
                                             #  "url": URL_OAUTH.format(APPID, quote('http://jianpianzi.com/mobile/logout'))}
                                             ]}]}
        data = JSONEncoder(ensure_ascii=False).encode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = response.read()
        result = jsonDecoder.decode(result)
        if 'errcode' in result:
            if result['errcode'] is not 0:
                return 'set menu failed, errorMsg:' + result['errmsg']
            return 'set menu success!'
        return 'network error'
    elif 'errmsg' in result:
        return result['errmsg']
    else:
        return 'network error'

# 微信所有消息推送到这
@weixing.route('/weixin', methods=['GET', 'POST'])
@incoming_params
def weixin():
    param = request.json_param

    # 微信服务器配置时的token验证
    if u'signature' in param and u'echostr' in param:
        signature = param[u'signature']
        timestamp = param[u'timestamp']
        nonce = param[u'nonce']
        echostr = param[u'echostr']

        #自己的token
        token="jianpianzi" #这里改写你在微信公众平台里输入的token

        #字典序排序
        list = [token, timestamp, nonce]
        list.sort()

        #sha1加密算法
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    return ''

#用于微信验证 on 2016-12-21
@weixing.route('/MP_verify_a19iolCUesS40hLm.txt', methods=['GET'])
def wx_js_safe_verify():
    return render_template('mobile/MP_verify_a19iolCUesS40hLm.txt')

#############内容操作#########################################

# 绑定已有账号(即登录)
class bind_wx_view(MethodView):
    decorators = [incoming_params]

    def get(self):
        param = request.json_param

        session['jump'] = param['path']
        return render_template('mobile/bindWX.html', path=param['path'])

    @staticmethod
    def post():
        param = request.json_param

        if len(param[u'Account']) <=0:
            return restfulApi.make_response({'bSuccess': False, 'error': u'empty user name'}, 200, headers='')

        if u'Domain' in param:
            if len(param[u'Domain']) <=0:
                return restfulApi.make_response({'bSuccess': False, 'error': u'empty domain name'}, 200, headers='')

            try:
                user = db.session.query(User).join(Domain, User.DomainId == Domain.Id)\
                    .filter(Domain.DomainName == param[u'Domain'])\
                    .filter(or_(User.DomainName == param[u'Account'], User.NickName == param[u'Account']))\
                    .filter(User.Password == param[u'Pwd']).one()
            except NoResultFound:
                return restfulApi.make_response({'bSuccess': False, 'error': u'wrong user account'}, 200, headers='')
        else:
            try:
                user = db.session.query(User).filter(User.Email == param[u'Account']).filter(User.Password == param[u'Pwd']).one()
            except NoResultFound:
                return restfulApi.make_response({'bSuccess': False, 'error': u'wrong user account'}, 200, headers='')


        if 'openId' in session:
            db.session.query(User).filter(User.WeiXinOpenId == session['openId']).update({User.WeiXinOpenId: ''})
            user.WeiXinOpenId = session['openId']
            db.session.commit()

        session['UserId'] = user.Id
        session['newLogin'] = True

        if 'jump' in session:
            del(session['jump'])

        return restfulApi.make_response({'bSuccess': True}, 200, headers='')

weixing.add_url_rule('/bindWX', view_func=bind_wx_view.as_view('bindWX'), methods=['GET', 'POST'])

# 注册新账号
class regist_wx_view(MethodView):
    decorators = [incoming_params]

    def get(self):
        param = request.json_param
        return render_template('mobile/register.html')

    @staticmethod
    @output_data_without_attribute(['MD5'])
    def post():
        param = request.form

        if param['phone'] == '':
            flash('请输入手机号')
            return render_template('mobile/register.html', phone=param['phone'], identityCode=param['IdentityCode'])
        if param['IdentityCode'] == '':
            flash('请输入验证码')
            return render_template('mobile/register.html', phone=param['phone'], identityCode=param['IdentityCode'])

        bPass = False
        registers = db.session.query(RegisterIdentity)\
            .filter(and_(RegisterIdentity.Email == param['phone'], RegisterIdentity.IdentityCode == param['IdentityCode'])).all()

        if registers.count() > 0:
            register = registers.one()
            duration = datetime.now() - register.CreateTime
            bPass = duration < timedelta(minutes=10)

            if bPass:
                users = User.query.filter_by( CellPhone = param['phone']).all()

                if users.count() == 0:
                    email = param['phone'] + '@FilmUnion.net'

                    user = User(None, email, param['phone'])
                    user.Password = hashlib.md5('Pass2Word').hexdigest()
                    user.Level = 1 #密码安全性低
                    user.DomainName = email
                    user.CellPhone = param['phone']
                    user.WeiXinOpenId = session['openId']
                    user.Status = 1 #在未有审核前，直接通过
                    user.type = 0 #普通用户
                    user.CreateTime = datetime.now()
                    user.LastLoginTime = datetime.now()

                    db.session.add(user)
                    db.session.flush()

                    domain = Domain(user.DomainName, user.Id)
                    domain.DefaultStorageSize = 1024 * 1024 * 1024
                    domain.UsedSize = 0
                    db.session.add(domain)

                    role = Role(u'超级管理员', None, user.Id, 1)
                    db.session.add(role)

                    user.Roles.append(role)
                    domain.Users.append(user)
                    domain.Roles.append(role)

                    rights = Right.query.all()
                    for right in rights:
                        if right.Leaf:
                            roleRight = RoleRight(right.Id, role.Id, 1)
                            db.session.add(roleRight)
                    rootobject = Object(param['email'], 1, 2, None, user.Id, user.Id, None)
                    db.session.add(rootobject)
                    db.session.flush()
                else:
                    user = users.one()
            else:
                flash('验证码已过期')
        else:
            flash('验证码不正确')

        registers.delete()
        db.session.commit()

        if bPass:
            session["UserId"] = user.Id
            session["DomainId"] = user.DomainId
            session["IsService"] = user.Domain.IsService

            newdirection = '/mobile/promote'
            if 'jump' in session:
                if session['jump'] != '':
                    newdirection = session['jump']
                del(session['jump']) #清空临时数据
            session['newLogin'] = True
            return redirect(newdirection)
        else:
            return render_template('mobile/register.html', phone=param['phone'], identityCode='')

weixing.add_url_rule('/registernewuser', view_func=regist_wx_view.as_view('register'), methods=['GET', 'POST'])

#验证邮箱是否重复
@weixing.route('/CheckEmail', methods=['GET', 'POST'])
def CheckEmail():
    try:
        db.session.query(User.Id).filter(User.Email == request.form['Email']).one()
    except NoResultFound:
        return 'true'
    return 'false'

#获取验证码
@weixing.route('/GetIdentityCode', methods=['GET', 'POST'])
@output_data
def GetIdentityCode():
    incoming = request.json_param

    emailaddress = incoming['Email']
    if len(emailaddress) == 0:
        return {"bSend": False, "ErrorInfo": "请输入邮箱" }

    try:
        db.session.query(User.Id).filter(User.Email == emailaddress).one()
    except:
        try:
            ri = db.session.query(RegisterIdentity).filter(RegisterIdentity.Email == emailaddress).one()
        except NoResultFound:
            ri = RegisterIdentity(emailaddress)
            db.session.add(ri)

        ri.IdentityCode = random.randint(100000, 999999)
        ri.CreateTime = datetime.now()
        body = "验证码：" + str(ri.IdentityCode) + "，请在10分钟内完成注册流程，否则验证码将过期";

        from Main import app
        try:
            MailSender.send_mail(app, body, "", [emailaddress], "商影联盟-注册验证码")
        except:
            return {"bSend": False, "ErrorInfo": "发送邮箱失败"}

        db.session.commit()
        return {"bSend": True, "IdentityCode": 0}
    return {"bSend": False, "ErrorInfo": "该邮箱已被注册" }

# 注销
@weixing.route('/logout', methods=['POST'])
@incoming_params
def removeWX():
    if 'UserId' in session:
        try:
            userid = session['UserId']

            if 'openId' in session:
                del(session['openId'])
            if 'UserId' in session:
                del(session['UserId'])

            user = User.query.filter_by(Id=userid).one()
            user.WeiXinOpenId = ""
            db.session.commit()
        except NoResultFound:
            pass

    return restfulApi.make_response({'bSuccess': False}, 200, headers='')

# 案例推荐
@weixing.route('/promote', methods=['GET'])
@incoming_params
@check_user
def mobile_promote():
    videos = db.session.query(ZoneItem)\
        .filter(and_(ZoneItem.Boutique!=0,ZoneItem.Type == ZoneItemType.Video))\
        .join(Object, Object.Id == ZoneItem.ObjectId)\
        .order_by(Object.ModifyTime.desc())\
        .limit(50).all()
    return render_template('mobile/promote.html', videos=videos)

# 媒体库
class media_view(MethodView):
    decorators = [output_data_without_attribute(['MD5']), incoming_params]

    @check_login2
    def get(self, parent_id):
        user = User.query.filter_by(Id=session['UserId']).one()
        pid = parent_id
        if not parent_id:
            try:
                root_object = Object.query.filter_by(ParentId=None, OwnerUserId=user.Id).one()
                pid = root_object.Id
            except NoResultFound:
                return render_template('mobile/media.html')

        level = pid
        level_tree = []
        count = 0
        while level and count<2:
            try:
                parent = Object.query.filter_by(Id=level).one()
            except NoResultFound:
                break
            cur_level = {'Id': parent.Id, 'Name': parent.Name}
            level_tree.append(cur_level)
            if not parent.ParentId:
                cur_level['Name'] = u'我的视频'
                break
            elif count ==1:
                cur_level['Name'] = u'...'
            level = parent.ParentId
            count += 1
        level_tree.reverse()

        page = 1
        per_page = 20
        pagination = Object.query.filter(and_(Object.OwnerUserId == user.Id, Object.ParentId == pid)).paginate(page, per_page)

        return render_template('mobile/media.html', Items=pagination.items, levels=level_tree, parentId=pid)

    @staticmethod
    @check_login
    def post(parent_id):
        param = request.json_param
        user = User.query.filter_by(Id=session['UserId']).one()
        pid = parent_id
        if not parent_id:
            try:
                root_object = Object.query.filter_by(ParentId=None, OwnerUserId=user.Id).one()
                pid = root_object.Id
            except NoResultFound:
                return {'bSuccess': False, 'error': u'no media info'}

        page = param[u'Page']
        per_page = 100
        pagination = Object.query.filter(and_(Object.OwnerUserId == user.Id, Object.ParentId == pid)).paginate(page, per_page)
        
        return {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
                'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
                'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}

mediaView = media_view.as_view('mediaView')
weixing.add_url_rule('/media', view_func=mediaView, defaults={'parent_id': None}, methods=['GET'])
weixing.add_url_rule('/media/<int:parent_id>', view_func=mediaView, methods=['GET'])
weixing.add_url_rule('/media/<int:parent_id>', view_func=mediaView, methods=['POST'])

# 需求管理
@weixing.route('/project/<string:filter>', methods=['GET'])
@incoming_params
@check_login2
def mobile_project(filter):
    user = User.query.filter_by(Id=session['UserId']).one()
    page = 1
    per_page = 50

    if user.Domain.IsService: # 制作商
        pagination = Requirement.query.join(ResourceShare, ResourceShare.ResourceId == Requirement.Id)\
            .filter(ResourceShare.ResourceType == 'r')\
            .filter(or_(ResourceShare.ShareDomainId == 0, ResourceShare.ShareDomainId == user.DomainId))

        rf = RequirementFollower.query.filter_by(FollowerDomainId=user.DomainId).all()
        req_ids = []
        for v in rf:
            req_ids.append(v.RequirementId)

        # 只查询和当前服务商相关的需求
        if filter == 'mine':
            print  user.Id
            pagination = Requirement.query\
            .filter(Requirement.ServiceUserId == user.Id) \
            .filter(Requirement.Status >= RequirementStatus.Published)
            # pagination = pagination.filter(
            #     Requirement.Id.in_(req_ids))\
            #     .filter(Requirement.Status >= RequirementStatus.Published)
        # 查询所有提交的需求
        elif filter == 'all':
            pagination = pagination.filter(Requirement.Status == RequirementStatus.Published)

        # 以创建时间倒序，分页
        pagination = pagination.order_by(Requirement.CreateTime.desc()).paginate(page, per_page)
        req = pagination.items
        req = expandAttribute(req, [])

        # 查询服务商对每个需求的申请状态
        for r in req:
            r['applyed'] = False
            for v in rf:
                if r['Id'] == v.RequirementId:
                    r['applyed'] = True
                    break
    else:
        pagination = Requirement.query\
            .join(User, Requirement.PublisherId == User.Id)\
            .filter(User.DomainId == user.DomainId)

        if filter == 'edit':
            pagination = pagination.filter(and_(Requirement.Status > RequirementStatus.Published,
                                                Requirement.Status < RequirementStatus.Last))
        elif filter == 'finish':
            pagination = pagination.filter(Requirement.Status == RequirementStatus.Last)
        elif filter == 'draft':
            pagination = pagination.filter(Requirement.Status == RequirementStatus.Created)

        pagination = pagination.order_by(Requirement.CreateTime.desc()).paginate(page, per_page)
        req = pagination.items
        req = expandAttribute(req, [])

    return render_template('mobile/project.html', IsService=user.Domain.IsService, reqs=req, filter=filter)


# 需求详情
@weixing.route('/requirement/<int:id>', methods=['GET'])
@incoming_params
@check_login2
def mobile_requirement(id):
    curId = id
    try:
        curuser = User.query.filter_by(Id=session['UserId']).one()
    except NoResultFound:
        return restfulApi.make_response({'bSuccess': False, 'error': u'not registed user!'}, 200, headers='')

    #不同的用户类型出现不同的页面
    if curuser.Domain.IsService:
        pass
        # return restfulApi.make_response({'bSuccess': False, 'error': u'not client!'}, 200, headers='')
        # return restfulApi.make_response({'bSuccess': False, 'error': u'您不是客户，服务商请从网站登陆!'}, 200, headers='')

    #Created+Published
    request = None
    try:
        request = Requirement.query \
            .filter(and_(User.DomainId == curuser.DomainId, Requirement.Id == curId)).one()
        #之前的只能客户端的人看到
            # .join(User, Requirement.PublisherId == User.Id)\
            # .filter(and_(User.DomainId == curuser.DomainId, Requirement.Id == curId)).one()
    except NoResultFound:
        return restfulApi.make_response({'bSuccess': False, 'error': u'not valid requiremnet ID!'}, 200, headers='')

    #Contracting
    #这个follower是很多钟方案
    follower = None
    print curId
    if request.Status >= RequirementStatus.Contracting:
        try:
            follower = RequirementFollower.query.filter_by(RequirementId=curId, IsDeny=0).all()

        except NoResultFound:
            pass
            # pass

    #PayDeposit
    rentOrder = None
    if request.Status >= RequirementStatus.PayDeposit:
        try:
            rentOrder = ContractOrder.query.filter_by(ContractId= request.ContractId, OrderType=ContractOrderType.PayRent).one()
        except NoResultFound:
            pass

    #Reviewing
    checkAttachment = None
    if request.Status >= RequirementStatus.Reviewing:
        try:
            checkAttachment = db.session.query(ContractAttachment)\
                .filter(ContractAttachment.ContractId == request.ContractId).all()
        except NoResultFound:
            pass

    #PayAll
    restOrder = None
    if request.Status >= RequirementStatus.PayAll:
        try:
            restOrder = ContractOrder.query.filter_by(ContractId= request.ContractId, OrderType=ContractOrderType.PayRest).one()
        except NoResultFound:
            pass

    #Retainage
    videoAttachment = None
    if request.Status >= RequirementStatus.Retainage:
        videoAttachment = db.session.query(ContractAttachment).\
            filter(ContractAttachment.ContractId == request.ContractId).all()
    return render_template('mobile/mrequirement.html',IsService=curuser.Domain.IsService,req=request,follower=follower,rentOrder=rentOrder,checkAttachment=checkAttachment,restOrder=restOrder,videoAttachment=videoAttachment)

@weixing.route('/deleteRequirement', methods=['POST'])
@incoming_params
def deleteRequirement():
    param={}
    param = request.json_param
    print param
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
        return 'ok'
    else:
        return APIException(SystemErrorCode.UnkonwnError, u'合同已经建立，无法删除需求')


@weixing.route('/publishRequirement', methods=['POST'])
@incoming_params
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
    # 取消提交
    if u'bCancel' in param:
        if requirement.Status == RequirementStatus.Published:
            requirement.Status = RequirementStatus.Created
            RequirementFollower.query.filter_by(RequirementId=requirement.Id).delete()
            db.session.commit()
        return requirement


    db.session.commit()
    return requirement

@weixing.route('/editRequirement/<int:id>', methods=['GET'])
@incoming_params
def editRequirement(id):
    try:
        req = Requirement.query \
            .filter(and_(Requirement.Id == id)).one()
        # 之前的只能客户端的人看到
        # .join(User, Requirement.PublisherId == User.Id)\
        # .filter(and_(User.DomainId == curuser.DomainId, Requirement.Id == curId)).one()
    except NoResultFound:
        return restfulApi.make_response({'bSuccess': False, 'error': u'not valid requiremnet ID!'}, 200, headers='')
    print req.Detail
    return render_template('mobile/editRequirement.html',req=req)

@weixing.route('/pay_notify', methods=['POST'])
@incoming_params
def payNotify():
    param = request.json_param
    if u'Id' in param:
        try:
            requirement = Requirement.query.filter_by(Id=param[u'Id']).one()
        except NoResultFound:
            raise APIException(SystemErrorCode.UnkonwnError, u'需求不存在')
        try:  # 合同押金支付
            print 'status'
            print requirement.Status
            if requirement.Status == RequirementStatus.PayDeposit:
                requirement.Status = RequirementStatus.Reviewing
                orderType = '合同押金'
            elif requirement.Status == RequirementStatus.PayAll:
                requirement.Status = RequirementStatus.Retainage
                orderType = '合同尾款'
            db.session.commit()
        except NoResultFound:
            pass
        return 'ok'




# ##################
# 申请需求
# ##################

@weixing.route('/askRequirement', methods=['GET', 'POST'])   #   申请需求并锁定
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


# ##################
# 提交需求
# ##################

def get_reqinfo(resource): #暂存需求信息到session
    @wraps(resource)
    def wrapper(*args, **kwargs):
        if 'reqParam' not in session:
            session['reqParam'] = request.json_param
        return resource(*args, **kwargs)
    return wrapper

class submit_view(MethodView):
    @incoming_params
    @check_user
    def get(self):
        param = request.json_param

        # 从注册页面跳转过来的
        if 'newLogin' in session and 'reqParam' in session:
            param = session['reqParam']
            del(session['newLogin'])
            submitreq(param)
            return redirect('mobile/project/mine')

        if 'newLogin' in session:
            del(session['newLogin'])
        if 'reqParam' in session:
            del(session['reqParam'])

        # 进需求提交页
        requirename = ''

        if u'requirename' in param:
            requirename = param[u'requirename']

        return render_template('mobile/submit.html',requirename=requirename)

    @incoming_params
    @check_login
    @get_reqinfo
    def post(self):
        param = session['reqParam']
        submitreq(param)
        return restfulApi.make_response({'bSuccess': True, 'Path': 'http://jianpianzi.com/mobile/project/mine'}, 200, headers='')

weixing.add_url_rule('/submit', view_func=submit_view.as_view('submit'), methods=['GET', 'POST'])

def submitreq(param):
    requirement = Requirement()
    if param[u'Status'] == 0:
        requirement.Status = 1
    else:
        requirement.Status = 2
    db.session.add(requirement)

    requirement.PublisherId = session['UserId']
    requirement.Title = param[u'Title']
    if u'long' in param:
        requirement.Long = param[u'Long']
    requirement.Amount = float(param[u'Amount'])
    requirement.Detail = param[u'Detail']
    requirement.Deadline = param[u'Deadline']
    if u'refer' in param:
        requirement.Refer = param[u'refer']
        requirement.ReferName = param[u'referName']
    db.session.flush()

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

    specifyDomains = param[u'specifyProducers']
    if len(specifyDomains) > 0:
        for d in specifyDomains:
            try:
                ResourceShare.query.filter_by(ResourceId=requirement.Id, ResourceType='r', ShareDomainId=d).one()
            except NoResultFound:
                r = ResourceShare(requirement.Id, 'r', d)
                db.session.add(r)
    else:
        try:
            ResourceShare.query.filter_by(ResourceId=requirement.Id, ResourceType='r', ShareDomainId=0).one()
        except NoResultFound:
            r = ResourceShare(requirement.Id, 'r', 0)
            db.session.add(r)
    db.session.commit()

    if 'reqParam' in session:
        del(session['reqParam'])


@weixing.route('/share/<objectid>')
@incoming_params
@weixin_refresh
@check_user
def share(objectid):
    try:
        object = db.session.query(Object).filter(Object.Id == objectid).one()

        bLogin = 'UserId' in session
        bShare = object.BShare

        zoneitem = None
        comments = None

        if not bShare:
            if not bLogin:
                return redirect('mobile/bindWX?path=http://jianpianzi.com/mobile/media')
            elif object.OwnerUserId <> session['UserId']:
                return redirect('mobile/media')
        else:
            zoneitem = db.session.query(ZoneItem).filter(ZoneItem.ObjectId == object.Id).one()
            zoneitem.ViewCount += 1
            db.session.commit()

            comments = CommentVideo.query.filter_by(ObjectId=object.Id).all()

        return render_template('mobile/share_video.html',
                   object=object, appId=APPID, logined=bLogin,
                   zone_item=zoneitem, comments=comments,
                   nonceStr=request.nonceStr, signature=request.signature, timestamp=request.timestamp)
    except:
         return render_template('mobile/help.html')

@weixing.route('/favorVideo', methods=['POST'])
@incoming_params
@check_login
def favor_video():
    incoming = request.json_param

    try:
        zi = ZoneItem.query.filter_by(Id=incoming[u'ZoneItemId']).one()
    except NoResultFound:
        return restfulApi.make_response({'bSuccess': False}, 200, headers='')

    try:
        db.session.query(Favortie).filter(
            and_(Favortie.ZoneItemId == incoming[u'ZoneItemId'],
                 Favortie.UserId == session['UserId'])).one()
    except NoResultFound:
        f = Favortie(incoming[u'ZoneItemId'], session['UserId'])
        db.session.add(f)

        zi.Favorite += 1
        db.session.commit()

    return restfulApi.make_response({'bSuccess': True, 'count': zi.Favorite}, 200, headers='')

@weixing.route('/help', methods=['GET'])
@incoming_params
def wxhelp():
    bregistered = 'UserId' in session
    return render_template('mobile/help.html', bregistered=bregistered)

@weixing.route('/aboutus', methods=['GET'])
@check_user
def wxaboutus():
    return render_template('mobile/aboutus.html')


