# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import datetime
import hashlib
from flask import Flask, Blueprint, render_template, abort, request, flash, redirect, url_for
from Models.Database import db
from Models.Index import Settings
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import and_, or_
from jinja2 import TemplateNotFound
from Models.CloudStorge import User, RegisterIdentity, Object, Domain, Role, Right, RoleRight
from Tools import MailSender
from Tools.DataPaser import output_data, method_post_only, output_data_without_attribute
from Tools.SqliteSession import ManualSession
login = Blueprint('login', __name__, template_folder='templates', static_folder='static')



@login.route('/login')
def LoginIndex():
    path = db.session.query(Settings).filter(Settings.Item == 'LoginImage').one().Value
    return render_template('login/login.html',path=path)


@login.route('/session')
def SessionIndex():
    return render_template('login/login.html')


@login.route('/register')
def Register():
    return render_template('login/register.html', register='true', user='')

# userUnverified = 0
# userVerified = 1

@login.route('/RegisterNewUser', methods=['GET', 'POST'])
@output_data_without_attribute(['MD5'])
def RegisterNewUser():
    if request.form['email'] == '':
        flash('请输入邮箱')
        return render_template('login/register.html', register='true', username=request.form['email'],
                               identityCode=request.form['IdentityCode'], user='')
    if request.form['pwd'] == '':
        flash('请输入密码')
        return render_template('login/register.html', register='true', username=request.form['email'],
                               identityCode=request.form['IdentityCode'], user='')
    if request.form['pwd'] != request.form['confirm-pwd']:
        flash('两次输入密码不一致')
        return render_template('login/register.html', register='true', username=request.form['email'],
                               identityCode=request.form['IdentityCode'], user='')
    try:
        request.form.getlist('protocol')[0] == 'on'
    except :
        flash('请同意《商影联盟用户注册协议》')
        return render_template('login/register.html', register='true', username=request.form['email'],
                               identityCode=request.form['IdentityCode'], user='')
    try:
        db.session.query(User.Id).filter(User.Email == request.form['email']).one()
        flash('该邮箱已被注册')
        return render_template('login/register.html', register='true', username=request.form['email'],
                               identityCode=request.form['IdentityCode'], user='')
    except NoResultFound:
        identityCode = request.form['IdentityCode']
        try:
            identity = db.session.query(RegisterIdentity).filter(RegisterIdentity.Email == request.form['email']).one()
        except NoResultFound:
            flash('验证码输入错误');
            return render_template('login/register.html', register='true', username=request.form['email'], user='')
        duration = datetime.datetime.now() - identity.CreateTime
        if duration > datetime.timedelta(minutes=10):
            flash('验证码已过期，请重新获取验证码')
            return render_template('login/register.html', register='true', username=request.form['email'], user='')
        if identityCode != identity.IdentityCode:
            flash('验证码错误');
            return render_template('login/register.html', register='true', username=request.form['email'], user='')

        user = User(None, request.form['email'], request.form['email'])
        Pwd = hashlib.md5(request.form['pwd']).hexdigest()
        user.Password = Pwd
        user.DomainName = request.form['email']
        #在未有审核前，直接通过
        user.Status = 1
        user.type = 0
        user.SessionId = ''
        user.CreateTime = datetime.datetime.now()
        s = request.form['pwd']
        if s.islower():
            level = 2
        else:
            level = 3
        if s.isnumeric() or s.isalpha():
            level = 1
        user.Level = level

        db.session.add(user)
        db.session.flush()

        #家庭组创建，暂时不校验共享云名称，不同用户可以含有共同的共享云名称
        # if Domain.query.filter_by(DomainName=param[u'DomainName']).count() > 0:
        #     return APIException(DataErrorCode.DomainNameExist, u'域名已被占用')
        domain = Domain(user.DomainName, user.Id)
        domain.DefaultStorageSize = 1024 * 1024 * 1024
        domain.UsedSize = 0
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

        rootobject = Object(request.form['email'], 1, 2, None, user.Id, user.Id, None)
        db.session.add(rootobject)
        #注册成功，清理验证码记录
        RegisterIdentity.query.filter_by(Email=request.form['email']).delete()

        ms = ManualSession()
        session = ms.open_session(create=True)
        if user.SessionId is not None and user.SessionId != session.sid:
            ms.close_session(sid=user.SessionId)
        user.SessionId = session.sid
        user.LastLoginTime = datetime.datetime.now()
        session["UserId"] = user.Id
        session["IsService"] = user.Domain.IsService
        session["CompanyName"] = user.Domain.CompanyName
        session["DBToken"] = session.sid
        session["NickName"] = user.NickName
        session["DomainName"] = user.DomainName
        session["DomainId"] = user.DomainId
        db.session.commit()
        return render_template('login/register_success.html', register='true', dbtoken=session.sid, user=user)


@login.route('/CheckEmail', methods=['GET', 'POST'])
def CheckEmail():
    try:
        db.session.query(User.Id).filter(User.Email == request.form['Email']).one()
    except NoResultFound:
        return 'true'
    return 'false'

@login.route('/GetIdentityCode', methods=['GET', 'POST'])
@output_data
def GetIdentityCode():
    if request.form['Email'] == '':
        return {"bSend": False, "ErrorInfo": "请输入邮箱" }
    try:
        db.session.query(User.Id).filter(User.Email == request.form['Email']).one()
    except:
        try:
            ri = db.session.query(RegisterIdentity).filter(RegisterIdentity.Email == request.form['Email']).one()
        except NoResultFound:
            ri = RegisterIdentity(request.form['Email'])
            db.session.add(ri)
        ri.IdentityCode = random.randint(100000, 999999)
        ri.CreateTime = datetime.datetime.now()
        body = "欢迎注册商影联盟！您的验证码为：" + str(ri.IdentityCode) + "，请在10分钟内完成注册流程，否则验证码将过期";

        from Main import app
        try:
            MailSender.send_mail(app, body, "", [request.form['Email']], "商影联盟-注册验证码")
        except:
            return {"bSend": False, "ErrorInfo": "发送邮箱失败"}
        db.session.commit()
        # return {"bSend": True, "IdentityCode": ri.IdentityCode}
        return {"bSend": True, "IdentityCode": 0} #不能把验证码返回
    return {"bSend": False, "ErrorInfo": "该邮箱已被注册" }

@login.route('/login/<page>')
def Show(page):
    try:
        return render_template('login/%s.html' % page)
    except TemplateNotFound:
        abort(404)

@login.route('/findpwd', methods=['GET', 'POST'])
def findpwd():
    return render_template('login/findpwd.html', user='')

@login.route('/GetPwdIdentityCode', methods=['GET', 'POST'])
@output_data
def GetPwdIdentityCode():
    if request.form['Email'] == '':
        return {"bSend": False, "ErrorInfo": "请输入邮箱" }
    try:
        db.session.query(User.Id).filter(User.Email == request.form['Email']).one()
        try:
            ri = db.session.query(RegisterIdentity).filter(RegisterIdentity.Email == request.form['Email']).one()
        except NoResultFound:
            ri = RegisterIdentity(request.form['Email'])
            db.session.add(ri)
        ri.IdentityCode = random.randint(100000, 999999)
        ri.CreateTime = datetime.datetime.now()
        body = "[重要信息]您正在找回商影联盟密码！您的验证码为：" + str(ri.IdentityCode) + "，请在10分钟内完成找回流程，否则验证码将过期。";

        from Main import app
        try:
            MailSender.send_mail(app, body, "", [request.form['Email']], "商影联盟-密码找回验证码")
        except:
            return {"bSend": False, "ErrorInfo": "发送邮箱失败"}
        db.session.commit()
        # return {"bSend": True, "IdentityCode": ri.IdentityCode}
        return {"bSend": True, "IdentityCode": 0} #不能把验证码返回
    except:
        return {"bSend": False, "ErrorInfo": "该邮箱并没有注册过，请确认。" }

@login.route('/FindPwd', methods=['GET', 'POST'])
@output_data_without_attribute(['MD5'])
def FindPwd():
    identityCode = request.form['FindPwdIdentityCode']
    try:
        identity = db.session.query(RegisterIdentity).filter(RegisterIdentity.Email == request.form['email']).one()
    except NoResultFound:
        flash('验证码错误');
        return redirect('findpwd')
    duration = datetime.datetime.now() - identity.CreateTime
    if duration > datetime.timedelta(minutes=10):
        flash('验证码已过期，请重新获取验证码')
        return redirect('findpwd')
    if identityCode != identity.IdentityCode:
        flash('验证码错误');
        return redirect('findpwd')
    return render_template('login/findpwd_next.html', email=request.form['email'],
                           identityCode = request.form['FindPwdIdentityCode'], user='')

@login.route('/ReSetPwd', methods=['GET', 'POST'])
@output_data_without_attribute(['MD5'])
def ReSetPwd():
    if request.form['pwd'] == '':
        flash('请输入密码')
        render_template('login/findpwd_next.html', email=request.form['email'],
                        identityCode = request.form['FindPwdIdentityCode'], user='')
    if request.form['pwd'] != request.form['confirm-pwd']:
        flash('两次输入密码不一致')
        render_template('login/findpwd_next.html', email=request.form['email'],
                        identityCode = request.form['FindPwdIdentityCode'], user='')

    user = db.session.query(User).filter(User.Email == request.form['email']).one()
    Pwd = hashlib.md5(request.form['pwd']).hexdigest()
    user.Password = Pwd
    s = request.form['pwd']
    if s.islower():
        level = 2
    else:
        level = 3
    if s.isnumeric() or s.isalpha():
        level = 1
    user.Level = level
    db.session.commit()
    return render_template('login/findpwd_success.html', user='')

@login.route('/checkDBToken', methods=['GET', 'POST'])
@output_data
def checkDBToken():
    param = request.json_param
    try:
        cookies = request.cookies
        user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
        return {'bSuccess': True}
    except NoResultFound:
        return {'bSuccess': False}

# 注册用户的账号状态
userUnverified = 0
userVerified = 1

@login.route('/SignIn', methods=['GET', 'POST'])
@output_data_without_attribute(['Password'])
@output_data
def SignIn():
    param = request.json_param
    if param[u'DomainName'] == '':
        try:
            user = db.session.query(User).filter(User.Email == param[u'UserName'], User.Password == param[u'Password']).one()
        except NoResultFound:
            return {"result": False, "info": u'用户名或密码错误'}
    else:
        try:
            user = db.session.query(User).join(Domain, User.DomainId == Domain.Id)\
                .filter(Domain.DomainName == param[u'DomainName'])\
                .filter(or_(User.DomainName == param[u'DomainUserName'], User.NickName == param[u'DomainUserName']))\
                .filter(User.Password == param[u'DomainPassword']).one()
        except NoResultFound:
            return {"result": False, "info": u'用户名或密码错误'}
    if user.Status == userUnverified:
        return {"result": False, "info": u'该用户账号尚未通过审核'}
    ms = ManualSession()
    session = ms.open_session(create=True)
    if user.SessionId is not None and user.SessionId != session.sid:
        ms.close_session(sid=user.SessionId)
    user.SessionId = session.sid
    user.LastLoginTime = datetime.datetime.now()
    db.session.commit()
    session["UserId"] = user.Id
    session["IsService"] = user.Domain.IsService
    session["CompanyName"] = user.Domain.CompanyName
    session["DBToken"] = session.sid
    session["NickName"] = user.NickName
    session["DomainName"] = user.DomainName
    session["DomainId"] = user.DomainId

    # tempRights = {}
    # if len(user.Roles) != 0:
    #     rolesId = []
    #     for role in user.Roles:
    #         rolesId.append(role.Id)
    #     result = RoleRight.query.filter(RoleRight.RoleId.in_(rolesId)).all()
    #     for r in result:
    #         tempRights[r.RightId] = 0
    #         tempRights[r.RightId] |= r.Checked

    # rights = Right.query.all()
    # userRights = {}
    # for right in rights:
    #     if right.Id in tempRights:
    #         userRights[right.Identity] = tempRights[right.Id]
    # respObj = {"DBToken": session.sid, "IsService": user.Domain.IsService, "NickName": user.NickName, "UserId": user.Id,
    #            "CompanyName": user.Domain.CompanyName, "DomainId": user.DomainId, "UserRights": userRights,
    #            "DomainInUse": user.Domain.Status == DomainStatus.use}
    from Main import api
    # from flask.ext.restful import unpack
    #
    # data, code, headers = unpack(respObj)
    resp = api.make_response({"result": True}, 200)
    resp.set_cookie("DBToken", session.sid)
    return resp
