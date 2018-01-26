#-*- coding: utf-8 -*-
import types
import hashlib
from urllib import urlencode, urlopen


# 基础信息配置
class AliPayConfig:
    # 商家合作者身份ID
    ALIPAY_PARTNERID = '2088811163391825'
    # 商家KEY
    ALIPAY_KEY = 'n0wpgo3333ix48ftzxg3zw25s24ylvot'
    # 商家支付宝账号
    ALIPAY_SELLER_EMAIL = 'zhh168_1@hotmail.com'
    # 参数签名方式
    ALIPAY_SIGN_TYPE = 'MD5'
    # 编码字符集
    ALIPAY_INPUT_CHARSET = 'utf-8'
    # 支付处理完成，异步通知商家后台的接口地址
    ALIPAY_NOTIFY_URL = 'http://jianpianzi.com/platform/aliPay_notify'
    #ALIPAY_NOTIFY_URL = 'http://localhost:5000/platform/aliPay_notify'
    # 支付处理完成，前端用户跳转到商户的网址
    ALIPAY_RETURN_URL = ''
    # 网关地址
    ALIPAY_GATEWAY = 'https://mapi.alipay.com/gateway.do?'


#字符串编解码处理
def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


# 对数组排序并除去数组中的空值和签名参数
# 返回数组和链接串
def params_filter(params):
    ks = params.keys()
    ks.sort()
    newParams = {}
    preStr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, AliPayConfig.ALIPAY_INPUT_CHARSET)
        if k not in ('sign','sign_type') and v != '':
            newParams[k] = smart_str(v, AliPayConfig.ALIPAY_INPUT_CHARSET)
            preStr += '%s=%s&' % (k, newParams[k])
    preStr = preStr[:-1]
    return newParams, preStr


# 生成签名结果
def build_mySign(preStr, key, sign_type='MD5'):
    if sign_type == 'MD5':
        return hashlib.md5(preStr + key).hexdigest()
    return ''


# 即时到账交易接口
def create_direct_pay_by_user(tn, subject, body, total_fee):
    params = {}
    params['service'] = 'create_direct_pay_by_user'
    #商品购买，只能选这个
    params['payment_type'] = '1'

    # 获取配置文件
    params['partner'] = AliPayConfig.ALIPAY_PARTNERID
    params['seller_id'] = AliPayConfig.ALIPAY_PARTNERID
    params['seller_email'] = AliPayConfig.ALIPAY_SELLER_EMAIL
    params['return_url'] = AliPayConfig.ALIPAY_RETURN_URL
    params['notify_url'] = AliPayConfig.ALIPAY_NOTIFY_URL
    params['_input_charset'] = AliPayConfig.ALIPAY_INPUT_CHARSET

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = tn         # 唯一订单号
    params['subject'] = subject         # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body               # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，可以为空
    params['total_fee'] = total_fee     # 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位
    params, preStr = params_filter(params)

    params['sign'] = build_mySign(preStr, AliPayConfig.ALIPAY_KEY, AliPayConfig.ALIPAY_SIGN_TYPE)
    params['sign_type'] = AliPayConfig.ALIPAY_SIGN_TYPE

    return AliPayConfig.ALIPAY_GATEWAY + urlencode(params)


def notify_verify(post):
    # 初级验证--签名
    _, preStr = params_filter(post)
    mySign = build_mySign(preStr, AliPayConfig.ALIPAY_KEY, AliPayConfig.ALIPAY_SIGN_TYPE)

    if mySign != post.get('sign'):
        return False

    # 二级验证--查询支付宝服务器此条信息是否有效
    params = {}
    params['partner'] = AliPayConfig.ALIPAY_PARTNERID
    params['notify_id'] = post.get('notify_id')

    gateway = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'
    verify_result = urlopen(gateway, urlencode(params)).read()
    if verify_result.lower().strip() == 'true':
        return True
    return False