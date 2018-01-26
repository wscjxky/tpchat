# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import hashlib
import datetime
from functools import wraps
from werkzeug import secure_filename
from flask import Flask, Blueprint, render_template, abort, request, flash, redirect, url_for, session
from flask.views import MethodView
from jinja2 import TemplateNotFound
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from sqlalchemy import and_
from Tools import DateCal
from Tools.DataPaser import output_data_without_attribute, incoming_params, output_data, expandAttribute
from Models.Database import db
from Models.CloudStorge import User, Domain, ManageStorage, PlatformSetting, ManageUser, Object, \
    Role, Right, RoleRight, DomainStatus, ManageTrade
from Models.Platform import *
from Models.Index import *
from flask.ext import restful
from Config import *

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def check_session():
    def wrapper_func_session(resource):
        @wraps(resource)
        def wrapper(*args, **kwargs):
            try:
                session['UserName']
            except:
                return redirect('admin')
            return resource(*args, **kwargs)
        return wrapper
    return wrapper_func_session


@admin.route('/admin')
def show():
    try:
        return render_template('admin/admin.html')
    except TemplateNotFound:
        abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@admin.route('/template/admin/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            banner = IndexBanner(filename, 'title', 'intro')
            db.session.add(banner)
            db.session.commit()
    return "ok"

@admin.route('/adminLogin', methods=['GET', 'POST'])
@output_data_without_attribute(['Password'])
def adminLogin():
    try:
        user = db.session.query(User).filter(User.Identity == 'admin').filter(
            User.Email == request.form['UserName'] and User.Password == request.form['Password']).one()
    except NoResultFound:
        flash(u'用户名或密码错误', 'error')
        return render_template('admin/admin.html')

    session['UserName'] = user.Email
    session["UserId"] = user.Id
    session["IsService"] = user.Domain.IsService
    session["CompanyName"] = user.Domain.CompanyName
    session["NickName"] = user.NickName
    session["DomainId"] = user.DomainId
    return redirect('admin/index')


@admin.route('/admin/logout')
@check_session()
def adminlogout():
    session.pop('UserName', None)
    return redirect('admin')



@admin.route('/admin/index')
@check_session()
def adminindex():
    userCount = User.query.count()
    customerCount = db.session.query(User).join(Domain, User.DomainId == Domain.Id)\
        .filter(Domain.IsService == 0).count()
    producerCount = db.session.query(User).join(Domain, User.DomainId == Domain.Id)\
        .filter(Domain.IsService == 1).count()

    latestTime = datetime.date.today() - datetime.timedelta(7)
    activeCustomerCount = db.session.query(User).join(Domain, User.DomainId == Domain.Id)\
        .filter(Domain.IsService == 0).filter(User.LastLoginTime > latestTime).count()
    activeProducerCount = db.session.query(User).join(Domain, User.DomainId == Domain.Id)\
        .filter(Domain.IsService == 1).filter(User.LastLoginTime > latestTime).count()
    params = {
        'userCount': userCount,
        'customerCount': customerCount,
        'producerCount': producerCount,
        'activeCustomerCount': activeCustomerCount,
        'activeProducerCount': activeProducerCount
    }
    return render_template('admin/admin_index.html', params=params)

class platformStorage_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        params = {}
        try:
            setting = PlatformSetting.query.one()
            result = db.session.query(func.max(ManageStorage.Id)).one()
            max_id = result[0]
            r = db.session.query(ManageStorage.UpdateTime).limit(1).one()
            min_year = r[0].year
            r = db.session.query(ManageStorage.UpdateTime).filter(ManageStorage.Id == max_id).one()
            max_year = r[0].year
            if max_id <= 12:
                storage_info = db.session.query(ManageStorage).all()
            else:
                step = max_id / 12
                id_group = []
                id = 1
                for i in range(0, 12, 1):
                    id_group.append(id)
                    id += step
                storage_info = db.session.query(ManageStorage).filter(ManageStorage.Id.in_(id_group)).all()

            time_category = []
            user_storage = []
            used_storage = []
            platform_storage = []
            for info in storage_info:
                time_category.append(info.UpdateTime.strftime('%Y-%m-%d'))
                user_storage.append(info.UserStorage / 1024 / 1024 / 1024)
                used_storage.append(info.UsedStorage / 1024 / 1024 / 1024)
                platform_storage.append(info.PlatformStorage / 1024 / 1024 / 1024)
            params['timeCategory'] = time_category
            params['userStorage'] = user_storage
            params['usedStorage'] = used_storage
            params['platformStorage'] = platform_storage
            params['curPlatformStorage'] = setting.StorageSize / 1024 / 1024 / 1024
            years = []
            while min_year <= max_year:
                years.append(min_year)
                min_year += 1
            params['years'] = years
        except NoResultFound:
            pass
        return render_template('admin/platform_storage.html', params=params)

    def post(self):
        incoming = request.json_param
        params = {}
        if incoming[u'filter'] == 'year':
            cur_year = incoming[u'year']
            storage_info = db.session.query(ManageStorage)\
                .filter(and_(ManageStorage.UpdateTime > datetime.date(cur_year-1, 12, 30),
                             ManageStorage.UpdateTime < datetime.date(cur_year+1, 1, 1))).all()
            time_category = []
            user_storage = []
            used_storage = []
            platform_storage = []
            for info in storage_info:
                if info.UpdateTime.day is not 23:
                    continue
                user_storage.append(info.UserStorage / 1024 / 1024 / 1024)
                used_storage.append(info.UsedStorage / 1024 / 1024 / 1024)
                platform_storage.append(info.PlatformStorage / 1024 / 1024 / 1024)
            for i in range(12):
                time_category.append(str(i + 1) + '月')
            params['timeCategory'] = time_category
            params['userStorage'] = user_storage
            params['usedStorage'] = used_storage
            params['platformStorage'] = platform_storage
        elif incoming[u'filter'] == 'month':
            cur_year = incoming[u'year']
            cur_month = incoming[u'month']
            storage_info = db.session.query(ManageStorage)\
                .filter(and_(ManageStorage.UpdateTime > DateCal.prev_month_last_day(cur_year, cur_month),
                             ManageStorage.UpdateTime < DateCal.next_month_first_day(cur_year, cur_month))).all()
            time_category = []
            user_storage = []
            used_storage = []
            platform_storage = []
            i = 1
            for info in storage_info:
                user_storage.append(info.UserStorage / 1024 / 1024 / 1024)
                used_storage.append(info.UsedStorage / 1024 / 1024 / 1024)
                platform_storage.append(info.PlatformStorage / 1024 / 1024 / 1024)
                time_category.append(i)
                i += 1

            params['timeCategory'] = time_category
            params['userStorage'] = user_storage
            params['usedStorage'] = used_storage
            params['platformStorage'] = platform_storage
        from Main import api
        resp = api.make_response(params, 200, headers='')
        return resp

admin.add_url_rule('/admin/platform/storage', view_func=platformStorage_view.as_view('platformStorage'))

@admin.route('/admin/platform/storage/search', methods=['POST'])
@output_data
def search():
    incoming = request.json_param
    searchPhase = "%" + incoming[u'filter'] + "%"
    #result = db.session.query(User).filter(User.DomainName.like(searchPhase)).all()
    result = db.session.query(User).join(Domain,User.DomainId == Domain.Id) \
            .filter(and_(User.Id == Domain.OwnerUserId,Domain.DomainName.like(searchPhase))).all()
    return render_template('admin/platform_storage_user.html', params=result)


@admin.route('/admin/platform/storage/update', methods=['POST'])
@check_session()
@output_data
def updateStorage():
    incoming = request.json_param
    setting = PlatformSetting.query.one()
    setting.StorageSize = incoming[u'storageSize'] * 1024 * 1024 * 1024
    db.session.commit()
    return incoming[u'storageSize']


@admin.route('/admin/platform/storage/updateUserSize', methods=['POST'])
@check_session()
@output_data
def updateUserStorage():
    incoming = request.json_param
    user = User.query.filter_by(Id=incoming[u'userId']).one()
    user.Domain.DefaultStorageSize = incoming[u'storageSize'] * 1024 * 1024 * 1024
    db.session.commit()
    return incoming[u'storageSize']

class platformApplyMoney_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        param = {}
        param['list'] = db.session.query(ApplyMoney).order_by(ApplyMoney.CreateTime).all()
        return render_template('admin/platform_apply.html', param=param)

    def post(self):
        incoming = request.json_param
        try:
            am = db.session.query(ApplyMoney).filter(ApplyMoney.Id == incoming[u'ApplyId']).one()
            am.Status = incoming[u'Status']
            if am.Status == 1:
                am.Domain.Count += am.Money
                log = '申请提现失败，请与平台运营人员联系'
                pm = PlatformMsg('申请提现', log, session['UserId'], am.UserId, 0, 'platform', 'applyMoney')
                db.session.add(pm)
            elif am.Status == 2:
                log = '申请提现成功，请及时查看个人账号'
                pm = PlatformMsg('申请提现', log, session['UserId'], am.UserId, 0, 'platform', 'applyMoney')
                db.session.add(pm)
                pass
            db.session.commit()
            from Main import api
            resp = api.make_response({'result': 'ok'}, 200, headers='')
            return resp
        except NoResultFound:
            from Main import api
            resp = api.make_response({'result': 'no record'}, 200, headers='')
            return resp


admin.add_url_rule('/admin/platform/apply', view_func=platformApplyMoney_view.as_view('platformApplyMoney'))


class leaveMsg_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        lm = LeaveMsg.query.all()
        return render_template('admin/platform_leaveMsg.html', param=lm)

    def post(self):
        incoming = request.json_param
        try:
            lm = LeaveMsg.query.filter_by(Id=incoming[u'Id']).one()
            lm.Deal = 1
            db.session.commit()
            from Main import api
            resp = api.make_response({'result': 'ok'}, 200, headers='')
            return resp
        except NoResultFound:
            from Main import api
            resp = api.make_response({'result': 'no record'}, 200, headers='')
            return resp


admin.add_url_rule('/admin/platform/leaveMsg', view_func=leaveMsg_view.as_view('leaveMsg_view'))



class platformTrade_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        params = {}
        try:
            result = db.session.query(func.max(ManageTrade.Id)).one()
            max_id = result[0]
            r = db.session.query(ManageTrade.UpdateTime).limit(1).one()
            min_year = r[0].year
            r = db.session.query(ManageTrade.UpdateTime).filter(ManageTrade.Id == max_id).one()
            max_year = r[0].year
            if max_id <= 12:
                trade_info = db.session.query(ManageTrade).all()
            else:
                step = max_id / 12
                id_group = []
                id = 1
                for i in range(0, 12, 1):
                    id_group.append(id)
                    id += step
                trade_info = db.session.query(ManageTrade).filter(ManageTrade.Id.in_(id_group)).all()

            time_category = []
            extend_storage_amount = []
            recharge_amount = []
            total_amount = []
            contract_amount = []
            tax_amount = []
            for info in trade_info:
                time_category.append(info.UpdateTime.strftime('%Y-%m-%d'))
                extend_storage_amount.append(info.ExtendStorageAmount)
                recharge_amount.append(info.RechargeAccountAmount)
                total_amount.append(info.TotalAmount)
                contract_amount.append(info.ContractAmount)
                tax_amount.append(info.MemberShipTaxAmount)
            params['timeCategory'] = time_category
            params['extendStorageAmount'] = extend_storage_amount
            params['rechargeAccountAmount'] = recharge_amount
            params['contractAmount'] = contract_amount
            params['totalAmount'] = total_amount
            params['memberShipTaxAmount'] = tax_amount
            years = []
            while min_year <= max_year:
                years.append(min_year)
                min_year += 1
            params['years'] = years
        except NoResultFound:
            pass
        return render_template('admin/platform_trade.html', params=params)

    def post(self):
        incoming = request.json_param
        params = {}
        if incoming[u'filter'] == 'year':
            cur_year = incoming[u'year']
            trade_info = db.session.query(ManageTrade)\
                .filter(and_(ManageTrade.UpdateTime > datetime.date(cur_year-1, 12, 30),
                             ManageTrade.UpdateTime < datetime.date(cur_year+1, 1, 1))).all()
            time_category = []
            extend_storage_amount = []
            recharge_amount = []
            total_amount = []
            contract_amount = []
            tax_amount = []
            for info in trade_info:
                if info.UpdateTime.day is not 21:
                    continue
                extend_storage_amount.append(info.ExtendStorageAmount)
                recharge_amount.append(info.RechargeAccountAmount)
                total_amount.append(info.TotalAmount)
                contract_amount.append(info.ContractAmount)
                tax_amount.append(info.MemberShipTaxAmount)
            for i in range(12):
                time_category.append(str(i + 1) + '月')
            params['timeCategory'] = time_category
            params['extendStorageAmount'] = extend_storage_amount
            params['rechargeAccountAmount'] = recharge_amount
            params['contractAmount'] = contract_amount
            params['totalAmount'] = total_amount
            params['memberShipTaxAmount'] = tax_amount
        elif incoming[u'filter'] == 'month':
            cur_year = incoming[u'year']
            cur_month = incoming[u'month']
            trade_info = db.session.query(ManageTrade)\
                .filter(and_(ManageTrade.UpdateTime > DateCal.prev_month_last_day(cur_year, cur_month),
                             ManageTrade.UpdateTime < DateCal.next_month_first_day(cur_year, cur_month))).all()
            time_category = []
            extend_storage_amount = []
            recharge_amount = []
            total_amount = []
            contract_amount = []
            tax_amount = []
            i = 1
            for info in trade_info:
                extend_storage_amount.append(info.ExtendStorageAmount)
                recharge_amount.append(info.RechargeAccountAmount)
                total_amount.append(info.TotalAmount)
                contract_amount.append(info.ContractAmount)
                tax_amount.append(info.MemberShipTaxAmount)
                time_category.append(i)
                i += 1

            params['timeCategory'] = time_category
            params['extendStorageAmount'] = extend_storage_amount
            params['rechargeAccountAmount'] = recharge_amount
            params['contractAmount'] = contract_amount
            params['totalAmount'] = total_amount
            params['memberShipTaxAmount'] = tax_amount
        from Main import api
        resp = api.make_response(params, 200, headers='')
        return resp

admin.add_url_rule('/admin/platform/trade', view_func=platformTrade_view.as_view('platformTrade'))


@admin.route('/admin/platform/trade/contractOrder')
@check_session()
@incoming_params
def contractOrder():
    incoming = request.json_param
    per_page = 20
    pagination = ContractOrder.query.paginate(int(incoming[u'page']), per_page)
    for item in pagination.items:
        if item.OrderType == ContractOrderType.PayRent:
            item.OrderType = '支付押金'
        elif item.OrderType == ContractOrderType.PayRest:
            item.OrderType = '支付尾款'
        if item.Order.State == OrderState.UnPay:
            item.Order.State = '未支付'
        elif item.Order.State == OrderState.Payed:
            item.Order.State = '已支付'
    params = {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
              'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
              'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}
    return render_template('admin/platform_trade_contractOrder.html', params=params)


@admin.route('/admin/platform/trade/contractOrder/<int:cid>')
@check_session()
@incoming_params
def contractOrder_id(cid):
    co = ContractOrder.query.filter_by(Id=cid).one()
    if co.OrderType == ContractOrderType.PayRent:
        co.OrderType = '合同：支付押金'
    elif co.OrderType == ContractOrderType.PayRest:
        co.OrderType = '合同：支付尾款'
    if co.Order.State == OrderState.UnPay:
        co.Order.State = '未支付'
    elif co.Order.State == OrderState.Payed:
        co.Order.State = '已支付'
    return render_template('admin/platform_trade_contractOrder_id.html', params=co)


@admin.route('/admin/platform/trade/rechargeOrder')
@check_session()
@incoming_params
def rechargeOrder():
    incoming = request.json_param
    per_page = 20
    pagination = RechargeAccountOrder.query.paginate(int(incoming[u'page']), per_page)
    for item in pagination.items:
        if item.Order.State == OrderState.UnPay:
            item.Order.State = '未支付'
        elif item.Order.State == OrderState.Payed:
            item.Order.State = '已支付'
    params = {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
              'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
              'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}
    return render_template('admin/platform_trade_rechargeOrder.html', params=params)


@admin.route('/admin/platform/trade/taxOrder')
@check_session()
@incoming_params
def taxOrder():
    incoming = request.json_param
    per_page = 20
    pagination = MemberShipTaxOrder.query.paginate(int(incoming[u'page']), per_page)
    for item in pagination.items:
        if item.Order.State == OrderState.UnPay:
            item.Order.State = '未支付'
        elif item.Order.State == OrderState.Payed:
            item.Order.State = '已支付'
    params = {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
              'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
              'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}
    return render_template('admin/platform_trade_taxOrder.html', params=params)


@admin.route('/admin/platform/trade/storageOrder')
@check_session()
@incoming_params
def storageOrder():
    incoming = request.json_param
    per_page = 20
    pagination = ExtendStorageOrder.query.paginate(int(incoming[u'page']), per_page)
    for item in pagination.items:
        if item.Order.State == OrderState.UnPay:
            item.Order.State = '未支付'
        elif item.Order.State == OrderState.Payed:
            item.Order.State = '已支付'
    params = {'HasNext': pagination.has_next, 'HasPrev': pagination.has_prev, 'Items': pagination.items,
              'Page': pagination.page, 'PageStep': pagination.per_page, 'Total': pagination.total,
              'Pages': pagination.pages, 'NextNum': pagination.next_num, 'PrevNum': pagination.prev_num}
    return render_template('admin/platform_trade_storageOrder.html', params=params)


@admin.route('/admin/platform/trade/order/<int:oid>')
@check_session()
@incoming_params
def order(oid):
    o = Order.query.filter_by(Id=oid).one()
    ol = OrderLog.query.filter(OrderLog.OrderId == o.Id).order_by(OrderLog.CreateTime).all()
    return render_template('admin/platform_trade_order.html', params=o, orderLog=ol)


@admin.route('/admin/platform/contract')
@check_session()
@incoming_params
def contract():
    car = ContractAbortRecord.query.all()
    return render_template('admin/platform_contract.html', params=car)


@admin.route('/admin/platform/contract/<int:cid>')
@check_session()
@incoming_params
def contractDetail(cid):
    c = Contract.query.filter_by(Id=cid).one()
    car = None
    try:
        car = ContractAbortRecord.query.filter_by(ContractId=cid).one()
    except NoResultFound:
        pass
    return render_template('admin/platform_contract_info.html', contract=c, record=car)


class user_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        params = {}
        try:
            result = db.session.query(func.max(ManageUser.Id)).one()
            max_id = result[0]
            result = db.session.query(ManageUser.UpdateTime).limit(1).one()
            min_year = result[0].year
            result = db.session.query(ManageUser.UpdateTime).filter(ManageUser.Id == max_id).one()
            max_year = result[0].year
            if max_id <= 12:
                user_info = db.session.query(ManageUser).all()
            else:
                step = max_id / 12
                id_group = []
                id = 1
                for i in range(0, 12, 1):
                    id_group.append(id)
                    id += step
                user_info = db.session.query(ManageUser).filter(ManageUser.Id.in_(id_group)).all()

            time_category = []
            customer_count = []
            producer_count = []
            for info in user_info:
                time_category.append(info.UpdateTime.strftime('%Y-%m-%d'))
                customer_count.append(info.CustomerCount)
                producer_count.append(info.ProducerCount)
            params['timeCategory'] = time_category
            params['customerCount'] = customer_count
            params['producerCount'] = producer_count
            years = []
            while min_year <= max_year:
                years.append(min_year)
                min_year += 1
            params['years'] = years
        except NoResultFound:
            pass
        return render_template('admin/user_general.html', params=params)

    def post(self):
        incoming = request.json_param
        params = {}
        if incoming[u'filter'] == 'year':
            cur_year = incoming[u'year']
            user_info = db.session.query(ManageUser)\
                .filter(and_(ManageUser.UpdateTime > datetime.date(cur_year-1, 12, 30),
                             ManageUser.UpdateTime < datetime.date(cur_year+1, 1, 1))).all()
            time_category = []
            customer_count = []
            producer_count = []
            for info in user_info:
                if info.UpdateTime.day is not 1:
                    continue
                customer_count.append(info.CustomerCount)
                producer_count.append(info.ProducerCount)
            for i in range(12):
                time_category.append(str(i + 1) + '月')
            params['timeCategory'] = time_category
            params['customerCount'] = customer_count
            params['producerCount'] = producer_count
        elif incoming[u'filter'] == 'month':
            cur_year = incoming[u'year']
            cur_month = incoming[u'month']
            user_info = db.session.query(ManageUser)\
                .filter(and_(ManageUser.UpdateTime > DateCal.prev_month_last_day(cur_year, cur_month),
                             ManageUser.UpdateTime < DateCal.next_month_first_day(cur_year, cur_month))).all()
            time_category = []
            customer_count = []
            producer_count = []
            i = 1
            for info in user_info:
                customer_count.append(info.CustomerCount)
                producer_count.append(info.ProducerCount)
                time_category.append(i)
                i += 1

            params['timeCategory'] = time_category
            params['customerCount'] = customer_count
            params['producerCount'] = producer_count
        from Main import api
        resp = api.make_response(params, 200, headers='')
        return resp

admin.add_url_rule('/admin/user', view_func=user_view.as_view('users'))

@admin.route('/admin/user/search')
@check_session()
@incoming_params
def userDetail():
    incoming = request.json_param
    if u'filter' not in incoming:
        return render_template('admin/user_search.html')
    searchPhase = "%" + incoming[u'filter'] + "%"
    #result = db.session.query(User).filter(User.DomainName.like(searchPhase)).all()
    result = db.session.query(User).join(Domain,User.DomainId == Domain.Id)\
             .filter(and_(User.Id == Domain.OwnerUserId,Domain.DomainName.like(searchPhase))).all()
    return render_template('admin/user_search.html', params=result)


@admin.route('/admin/user/<int:uid>')
@check_session()
@incoming_params
def user_id(uid):
    user = User.query.filter_by(Id=uid).one()
    if user.Domain.IsService:
        contract = Contract.query.filter_by(ServiceUserId=user.Id).all()
    else:
        contract = Contract.query.filter_by(CustomerUserId=user.Id).all()

    co = db.session.query(ContractOrder).join(Order, Order.Id == ContractOrder.OrderId).filter(Order.PayUserId == uid).all()
    rao = RechargeAccountOrder.query.join(Order, Order.Id == RechargeAccountOrder.OrderId).filter(Order.PayUserId == uid).all()
    eso = ExtendStorageOrder.query.join(Order, Order.Id == ExtendStorageOrder.OrderId).filter(Order.PayUserId == uid).all()
    msto = MemberShipTaxOrder.query.join(Order, Order.Id == MemberShipTaxOrder.OrderId).filter(Order.PayUserId == uid).all()
    params = {'user': user, 'contract': contract, 'contractOrder': co,
              'rechargeOrder': rao, 'storageOrder': eso, 'taxOrder': msto}
    return render_template('admin/user_info.html', params=params)


@admin.route('/admin/user/addProducer', methods=['POST'])
@check_session()
@output_data
def addProducer():
    incoming = request.json_param
    search = '%' + incoming[u'companyName'] + '%'
    try:
        Domain.query.filter(Domain.CompanyName.like(search)).one()
        return {'result': 'exist'}
    except NoResultFound:
        user = User(None, incoming[u'email'], incoming[u'email'])
        Pwd = hashlib.md5(incoming[u'pwd']).hexdigest()
        user.Password = Pwd
        user.DomainName = incoming[u'companyName']
        #在未有审核前，直接通过
        user.Status = 1
        user.type = 0
        user.SessionId = ''
        user.CellPhone = incoming[u'cellPhone']
        user.CreateTime = datetime.datetime.now()
        s = incoming[u'pwd']
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
        domain = Domain(user.DomainName, user.Id)
        domain.DefaultStorageSize = 1024 * 1024 * 1024
        domain.UsedSize = 0
        domain.IsService = 1
        domain.ExpireTime = datetime.date.today() + datetime.timedelta(30 * int(incoming[u'rewardTime']))
        domain.CompanyCelPhone = incoming[u'cellPhone']
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

        rootobject = Object(incoming[u'email'], 1, 2, None, user.Id, user.Id, None)
        db.session.add(rootobject)
        db.session.commit()
        return {'result': 'success'}


class promoteActivity_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        params = IndexBanner.query.all()
        return render_template('admin/promote_activity.html', params=params)

    def post(self):
        incoming = request.json_param
        IndexBanner.query.delete()
        for v in incoming[u'group']:
            b = IndexBanner(v[u'name'], v[u'path'], v[u'page'])
            db.session.add(b)
        db.session.commit()
        from Main import api
        resp = api.make_response('', 200, headers='')
        return resp

admin.add_url_rule('/admin/promote/activity', view_func=promoteActivity_view.as_view('promote_activity'))


class promoteChannel_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        c_1 = Category.query.filter_by(Level=1).all()
        curC1 = c_1[0]
        c_2 = Category.query.filter_by(Level=2, ParentId=curC1.Id).all()
        c2Name = ''
        if c_2:
            curC2 = c_2[0]
            c2Name = curC2.Name
        c1Group = db.session.query(ChannelSetting).filter(ChannelSetting.ParentId == None)\
            .order_by(ChannelSetting.Position).all()
        c2Group = db.session.query(ChannelSetting).filter(ChannelSetting.ParentId == curC1.Id)\
            .order_by(ChannelSetting.Position).all()
        params = {'c1': c_1, 'c2': c_2, 'curC1': curC1.Name, 'curC2': c2Name, 'curC1Ex': '',
                  'c1Group': c1Group, 'c2Group': c2Group}
        return render_template('admin/promote_channel.html', params=params)

    def post(self):
        incoming = request.json_param
        curC1_name = incoming[u'curC1']
        curC1Ex_name = incoming[u'curC1Ex']
        curC2_name = incoming[u'curC2']
        targetName = incoming[u'targetName']
        operator = incoming[u'operator']
        level = incoming[u'level']

        c1 = Category.query.filter_by(Name=curC1_name).one()
        c1Ex = None
        try:
            c1Ex = Category.query.filter_by(Name=curC1Ex_name).one()
        except NoResultFound:
            pass
        c1s = Category.query.filter_by(Level=1).all()
        c2s = Category.query.filter_by(Level=2, ParentId=c1.Id).all()
        if operator == 'changeC2':
            curC2_name = c2s[0].Name
        elif operator == 'add':
            target = Category.query.filter_by(Name=targetName).one()
            try:
                ChannelSetting.query.filter_by(CategoryId=target.Id).one()
            except NoResultFound:
                pos = db.session.query(func.max(ChannelSetting.Position))\
                    .filter(ChannelSetting.ParentId == target.ParentId).one()
                pos = pos[0]
                if pos is None:
                    pos = 1
                add = ChannelSetting(target.Id, pos + 1, target.Name, target.ParentId)
                db.session.add(add)
                db.session.flush
                db.session.commit()
        elif operator == 'del':
            target = Category.query.filter_by(Name=targetName).one()
            try:
                delItem = ChannelSetting.query.filter_by(CategoryId=target.Id).one()
                db.session.delete(delItem)
                db.session.commit()
            except NoResultFound:
                pass
        elif operator == 'new':
            if level == 1:
                try:
                    Category.query.filter_by(Name=targetName).one()
                except NoResultFound:
                    newC1 = Category()
                    newC1.Level = 1
                    newC1.Name = targetName
                    db.session.add(newC1)
                    db.session.flush()
                    db.session.commit()
            else:
                try:
                    Category.query.filter_by(Name=targetName).one()
                except NoResultFound:
                    newC2 = Category()
                    newC2.Level = 2
                    newC2.Name = targetName
                    newC2.ParentId = c1Ex.Id
                    db.session.add(newC2)
                    db.session.flush()
                    db.session.commit()
        elif operator == 'remove':
            if level == 1:
                delItem = Category.query.filter_by(Name=targetName).one()
                ChannelSetting.query.filter_by(CategoryId=delItem.Id).delete()
                RequirementTemplate.query.filter_by(Category_1=delItem.Id).delete()
                Category.query.filter_by(ParentId=delItem.Id).delete()
                db.session.delete(delItem)
                db.session.commit()
            else:
                delItem = Category.query.filter_by(Name=targetName).one()
                ChannelSetting.query.filter_by(CategoryId=delItem.Id).delete()
                RequirementTemplate.query.filter_by(Category_2=delItem.Id).delete()
                db.session.delete(delItem)
                db.session.commit()

        c1s = Category.query.filter_by(Level=1).all()
        c2s = Category.query.filter_by(Level=2, ParentId=c1.Id).all()
        c2sEx = []
        if c1Ex:
            c2sEx = db.session.query(Category).filter(Category.ParentId == c1Ex.Id).all()
        c1Group = db.session.query(ChannelSetting).filter(ChannelSetting.ParentId == None)\
            .order_by(ChannelSetting.Position).all()
        c2Group = db.session.query(ChannelSetting).filter(ChannelSetting.ParentId == c1.Id)\
            .order_by(ChannelSetting.Position).all()
        params = {'c1': c1s, 'c2': c2s, 'curC1': curC1_name, 'curC2': curC2_name, 'curC1Ex': curC1Ex_name,
                  'c1Group': c1Group, 'c2Group': c2Group, 'c2Ex': c2sEx}
        data = render_template('admin/promote_channel_sub.html', params=params)
        from Main import api
        resp = api.make_response(data, 200, headers='')
        return resp

admin.add_url_rule('/admin/promote/channel', view_func=promoteChannel_view.as_view('promote_channel'))


class promoteClassical_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        applying = ZoneItem.query.filter_by(Classical=ZoneItemClassicalStatus.applying).all()
        applySuccess = ZoneItem.query.filter_by(Classical=ZoneItemClassicalStatus.applySuccuss).all()
        cs = ClassicalSetting.query.all()
        c = Category.query.filter_by(Level=1).all()
        applying = expandAttribute(applying, ['Object'])
        applySuccess = expandAttribute(applySuccess, ['Object'])
        cMap = {}
        for cate in c:
            cMap[cate.Id] = cate.Name
        for item in applying:
            item["category"] = cMap[item["Object"].Category_1]
        for item2 in applySuccess:
            item2["category"] = cMap[item2["Object"].Category_1]

        sortByCategory = {}
        for item3 in applySuccess:
            category_1 = item3["category"]
            if category_1 in sortByCategory:
                sortByCategory[category_1].append(item3)
            else:
                sortByCategory[category_1] = [item3]
        params = {'applying': applying, 'classicalList': cs, 'applySuccess': applySuccess, 'sortByCategory': sortByCategory}
        return render_template('admin/promote_classical.html', params=params)

    def post(self):
        incoming = request.json_param
        if incoming[u'operator'] == 'pass':
            z = ZoneItem.query.filter_by(Id=incoming[u'targetId']).one()
            z.Classical = ZoneItemClassicalStatus.applySuccuss
            db.session.commit()
        elif incoming[u'operator'] == 'deny':
            z = ZoneItem.query.filter_by(Id=incoming[u'targetId']).one()
            z.Classical = ZoneItemClassicalStatus.applyDeny
            db.session.commit()
        elif incoming[u'operator'] == 'add':
            cs = db.session.query(func.max(ClassicalSetting.Position)).one()
            try:
                ClassicalSetting.query.filter_by(ZoneItemId=incoming[u'targetId']).one()
            except NoResultFound:
                pos = cs[0]
                if pos is None:
                    pos = 1
                add = ClassicalSetting(incoming[u'targetId'], pos + 1)
                zi = ZoneItem.query.filter_by(Id=incoming[u'targetId']).one()
                zi.Price = -1
                db.session.add(add)
                db.session.commit()
        elif incoming[u'operator'] == 'del':
            # ClassicalSetting.query.filter_by(ZoneItemId=incoming[u'targetId']).delete()
            zi = ZoneItem.query.filter_by(Id=incoming[u'targetId']).one()
            zi.Classical = 1
            # zi.Price = 0
            db.session.commit()
        elif incoming[u'operator'] == 'modifyWeight':
            zi = ZoneItem.query.filter_by(Id=incoming[u'targetId']).one()
            zi.ClassicalWeight = incoming[u'Weight']
            db.session.commit()
        from Main import api
        resp = api.make_response('', 200, headers='')
        return resp

admin.add_url_rule('/admin/promote/classical', view_func=promoteClassical_view.as_view('promoteClassical'))


class promoteShare_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        applyAll = db.session.query(ZoneItem).join(Domain, Domain.Id == ZoneItem.DomainId)\
            .filter(Domain.ShowType !=0)\
            .order_by(ZoneItem.ClassicalWeight.desc()).all()
        c = Category.query.filter_by(Level=1).all()
        applyAll = expandAttribute(applyAll, ['Object'])
        cMap = {}
        for cate in c:
            cMap[cate.Id] = cate.Name
        for item2 in applyAll:
            if item2["Object"] and item2["Object"].Category_1 and cMap.has_key(item2["Object"].Category_1):
                item2["category"] = cMap[item2["Object"].Category_1]

        sortByCategory = {}
        for item3 in applyAll:
            if "category" not in item3:
                continue
            category_1 = item3["category"]
            if category_1 in sortByCategory:
                sortByCategory[category_1].append(item3)
            else:
                sortByCategory[category_1] = [item3]
        params = {'sortByCategory': sortByCategory}
        return render_template('admin/promote_share.html', params=params)

    def post(self):
        incoming = request.json_param
        if incoming[u'operator'] == 'modifyWeight':
            zi = ZoneItem.query.filter_by(Id=incoming[u'targetId']).one()
            zi.ClassicalWeight = incoming[u'Weight']
            db.session.commit()
        from Main import api
        resp = api.make_response('', 200, headers='')
        return resp

admin.add_url_rule('/admin/promote/share', view_func=promoteShare_view.as_view('promoteShare'))

class promoteBoutique_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        applyAll = db.session.query(ZoneItem).join(Domain, Domain.Id == ZoneItem.DomainId)\
            .filter(Domain.ShowType !=0)\
            .order_by(ZoneItem.ClassicalWeight.desc()).all()
        c = Category.query.filter_by(Level=1).all()
        applyAll = expandAttribute(applyAll, ['Object'])
        cMap = {}
        for cate in c:
            cMap[cate.Id] = cate.Name
        for item2 in applyAll:
            if item2["Object"] and item2["Object"].Category_1 and cMap.has_key(item2["Object"].Category_1):
                item2["category"] = cMap[item2["Object"].Category_1]

        sortByCategory = {}
        for item3 in applyAll:
            if "category" not in item3:
                continue
            category_1 = item3["category"]
            if category_1 in sortByCategory:
                sortByCategory[category_1].append(item3)
            else:
                sortByCategory[category_1] = [item3]
        params = {'sortByCategory': sortByCategory}
        return render_template('admin/promote_boutique.html', params=params)

    def post(self):
        incoming = request.json_param
        if incoming[u'operator'] == 'modifyBoutique':
            zi = ZoneItem.query.filter_by(Id=incoming[u'targetId']).one()
            if incoming[u'Boutique']==0 or incoming[u'Boutique'] == 1:
                zi.Boutique = incoming[u'Boutique']
                db.session.commit()
        from Main import api
        resp = api.make_response('', 200, headers='')
        return resp

admin.add_url_rule('/admin/promote/boutique', view_func=promoteBoutique_view.as_view('promoteBoutique'))

class promoteProducer_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        incoming = request.json_param
        searchUsers = []
        if u'search' in incoming:
            searchPhase = "%" + incoming[u'search'] + "%"
            searchUsers = db.session.query(Domain)\
                .filter(and_(Domain.CompanyName.like(searchPhase), Domain.IsService == 1, Domain.ShowType == 1)).all()
        #producers = ProducerSetting.query.all()
        producers = db.session.query(Domain).filter(and_(Domain.IsService == 1, Domain.ShowType == 2)).all()
        producer_visable = Settings.query.filter_by(Item='isProducerVisable').one().Value
        params = {'producers': producers, 'searchUsers': searchUsers,'producer_visable':producer_visable}
        return render_template('admin/promote_producer.html', params=params)

    def post(self):
        incoming = request.json_param
        if incoming[u'operator'] == 'add':
            #try:
            #   ProducerSetting.query.filter_by(DomainId=incoming[u'targetId']).one()
            #except NoResultFound:
            #   cs = db.session.query(func.max(ProducerSetting.Position)).one()
            #   pos = cs[0]
            #   if pos is None:
            #       pos = 1
            #   p = ProducerSetting(incoming[u'targetId'], pos + 1)
            d = Domain.query.filter_by(Id=incoming[u'targetId']).one()
            d.Price = -1
            d.ShowType = 2
            #db.session.add(p)
            db.session.commit()
        elif incoming[u'operator'] == 'del':
            #ProducerSetting.query.filter_by(DomainId=incoming[u'targetId']).delete()
            d = Domain.query.filter_by(Id=incoming[u'targetId']).one()
            d.Price = 0
            d.ShowType = 1
            db.session.commit()
        from Main import api
        resp = api.make_response('', 200, headers='')
        return resp

admin.add_url_rule('/admin/promote/producer', view_func=promoteProducer_view.as_view('promoteProducer'))


class promoteUser_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        incoming = request.json_param
        searchUsers = []
        if u'search' in incoming:
            searchPhase = "%" + incoming[u'search'] + "%"
            #searchUsers = db.session.query(User).filter(and_(User.Email.like(searchPhase), User.type == 0)).all()
            searchUsers = db.session.query(Domain).filter(and_(Domain.CompanyName.like(searchPhase), Domain.IsService == 0, Domain.ShowType == 1)).all()
        users = db.session.query(Domain).filter(and_(Domain.IsService == 0, Domain.ShowType == 2)).all()
        #users = db.session.query(User).filter(User.type == 1).all()
        params = {'users': users, 'searchUsers': searchUsers}
        return render_template('admin/promote_user.html', params=params)

    def post(self):
        incoming = request.json_param
        if incoming[u'operator'] == 'add':
            #user = User.query.filter_by(Id=incoming[u'targetId']).one()
            #user.type = 1
            user = Domain.query.filter_by(Id=incoming[u'targetId']).one()
            user.ShowType = 2
            db.session.commit()
        elif incoming[u'operator'] == 'del':
            #user = User.query.filter_by(Id=incoming[u'targetId']).one()
            #user.type = 0
            user = Domain.query.filter_by(Id=incoming[u'targetId']).one()
            user.ShowType = 1
            db.session.commit()
        from Main import api
        resp = api.make_response('', 200, headers='')
        return resp

admin.add_url_rule('/admin/promote/user', view_func=promoteUser_view.as_view('promoteUser'))

@admin.route('/admin/promote/channel/template/<int:cid>')
@check_session()
def addChannelTemplate(cid):
    try:
        c = Category.query.filter_by(Id=cid).one()
    except NoResultFound:
        return render_template('admin/promote_channel_template.html')

    parent = Category.query.filter_by(Id=c.ParentId).one()
    params = {}
    try:
        rt = RequirementTemplate.query.filter_by(Category_2=c.Id).one()
    except NoResultFound:
        rt = RequirementTemplate(parent.Id, c.Id, '')
        db.session.add(rt)
        db.session.commit()
        rt.Id
    params['category_1'] = parent
    params['category_2'] = c
    params['rTemplate'] = rt
    return render_template('admin/promote_channel_template.html', params=params)


@admin.route('/admin/promote/channel/template', methods=['POST'])
@check_session()
@output_data
def modifyTemplate():
    incoming = request.json_param
    if incoming[u'operator'] == 'save':
        rt = RequirementTemplate.query.filter_by(Category_2=incoming[u'c2Id']).one()
        rt.Detail = incoming[u'detail']
    elif incoming[u'operator'] == 'del':
        RequirementTemplate.query.filter_by(Category_2=incoming[u'c2Id']).delete()
    db.session.commit()
    return {}


@admin.route('/admin/sendSysMsgToUser', methods=['POST'])
@check_session()
@output_data
def sendSysMsgToUser():
    incoming = request.json_param
    pm = PlatformMsg(incoming[u'title'], incoming[u'content'], session['UserId'], incoming[u'userId'], -1, 'system', 'msg')
    db.session.add(pm)
    db.session.commit()
    return {}


@admin.route('/admin/setDomainVisible', methods=['POST'])
@check_session()
@output_data
def setDomainVisible():
    incoming = request.json_param
    d = Domain.query.filter_by(Id=incoming[u'DomainId']).one()
    d.ShowType = incoming[u'ShowType']
    db.session.commit()
    return {}

@admin.route('/admin/setProducerVisible', methods=['POST'])
@check_session()
@output_data
def setProducerVisible():
    incoming = request.json_param
    producer_visable = Settings.query.filter_by(Item='isProducerVisable').one()
    producer_visable.Value = incoming[u'Value']
    db.session.commit()
    return {}


class promoteLogin_view(MethodView):
    decorators = [check_session(), incoming_params]

    def get(self):
        try:
            li = db.session.query(Settings).filter(Settings.Item == 'LoginImage').one()
            path = li.Value
        except NoResultFound:
            path = ''
        return render_template('admin/promote_login.html', path=path)

    def post(self):
        incoming = request.json_param
        try:
            li = db.session.query(Settings).filter(Settings.Item == 'LoginImage').one()
            li.Value = incoming[u'path']
        except NoResultFound:
            li = Settings('LoginImage', incoming[u'path'])
            db.session.add(li)
        db.session.commit()
        from Main import api
        resp = api.make_response('', 200)
        return resp

admin.add_url_rule('/admin/promote/login', view_func=promoteLogin_view.as_view('promoteLogin'))


@admin.route('/admin/confirmAbortContract', methods=['POST'])
@check_session()
@output_data
def confirmAbortContract():
    param = request.json_param
    car = ContractAbortRecord.query.filter_by(ContractId=param[u'ContractId']).one()
    c = Contract.query.filter_by(Id=param[u'ContractId']).one()
    car.ConfirmRemark = param[u'ConfirmRemark']
    car.ConfirmTime = datetime.datetime.now()
    if param[u'Deny']:
        c.Procedure = 'active'
        car.Status = 'deny'
        return {'bSuccess': True}
    else:
        c.Procedure = 'abort'
        car.Status = 'abort'
    if c.Status >= ContractStatus.ContractCompleted:
        c.CustomerUser.Domain.Count += c.Amount
    elif c.Status >= ContractStatus.ContractStart:
        c.CustomerUser.Domain.Count += c.Amount * c.DepositPercent
    db.session.commit()
    return {'bSuccess': True}


@admin.route('/admin/abortingContract', methods=['GET'])
@check_session()
@incoming_params
def abortingContract():
    car = ContractAbortRecord.query.filter_by(Status='apply').all()
    return car

@admin.route('/admin/resetpwd', methods=['POST'])
@check_session()
@output_data
def setPwd():
    incoming = request.json_param
    # d = Domain.query.filter_by(Id=incoming[u'DomainId']).one()
    user = User.query.filter_by(Id=incoming[u'userId']).one()
    defpwd = u'Pass2Word'
    user.Password = hashlib.md5(defpwd.encode('utf-8')).hexdigest()
    user.Level = 3
    db.session.commit()
    return {}
