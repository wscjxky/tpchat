<?php
/**
 * Created by PhpStorm.
 * User: hhh
 * Date: 2017/8/14
 * Time: 下午4:14
 */

namespace Home\Controller;
ini_set('date.timezone','Asia/Shanghai');
use Think\Controller;


class JspayController extends Controller
{
    public function index()
    {
        vendor('Wechat.WxPayJsApiPay');
        vendor('Wechat.WxPayApi');
        vendor('Wechat.log');
        $logHandler = new \CLogFileHandler("../logs/" . date('Y-m-d') . '.log');
        $log = \Log::Init($logHandler, 15);

        //打印输出数组信息
        function printf_info($data)
        {
            foreach ($data as $key => $value) {
                echo "<font color='#00ff55;'>$key</font> : $value <br/>";
            }
        }

        //①、获取用户openid
        $tools = new \JsApiPay();
        $openId = $tools->GetOpenid();

        //获取课程名称
        $course = D('trade');
        $trade_id = I('get.trade_id');
        $data = $course->where(array("trade_id" => $trade_id))->find();
        $this->assign('data', $data);


        //②、统一下单
        $input = new \WxPayUnifiedOrder();
        $input->SetBody("远途文化");
        $input->SetAttach($data['trade_id']."");
        $input->SetOut_trade_no(\WxPayConfig::MCHID . date("YmdHis"));
        $input->SetTotal_fee((int)$data['final_price']*100);
//        $input->SetTotal_fee(1);
        $input->SetTime_start(date("YmdHis"));
        $input->SetTime_expire(date("YmdHis", time() + 600));
        $input->SetGoods_tag("test");
        $input->SetNotify_url("http://www.cunpianzi.com/tpchat/example/notify.php");
        $input->SetTrade_type("JSAPI");
        $input->SetOpenid($openId);
        $order = \WxPayApi::unifiedOrder($input);

        //printf_info($order);
        $jsApiParameters = $tools->GetJsApiParameters($order);

        //获取共享收货地址js函数参数
        $editAddress = $tools->GetEditAddressParameters();

        //③、在支持成功回调通知中处理成功之后的事宜，见 notify.php
        /**
         * 注意：
         * 1、当你的回调地址不可访问的时候，回调通知会失败，可以通过查询订单来确认支付是否成功
         * 2、jsapi支付时需要填入用户openid，WxPay.JsApiPay.php中有获取openid流程 （文档可以参考微信公众平台“网页授权接口”，
         * 参考http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html）
         */
        echo sprintf('
            
            <html>
            <head>
               
                <script type="text/javascript">
                    //调用微信JS api 支付
                    function jsApiCall()
                    {
                        WeixinJSBridge.invoke(
                            "getBrandWCPayRequest",
                            %s,
                            function(res){
                                WeixinJSBridge.log(res.err_msg);
                                 if(res.err_msg == "get_brand_wcpay_request:ok" ){
                                         window.location.href="http://www.cunpianzi.com/tpchat/index.php/home/result?trade_id=%s"; 
           				           }
           				           else{

           				           }
                            }
           				           
                                                )
                    }
            
                    function callpay()
                    {
                        if (typeof WeixinJSBridge == "undefined"){
                            if( document.addEventListener ){
                                document.addEventListener("WeixinJSBridgeReady", jsApiCall, false);
                            }else if (document.attachEvent){
                                document.attachEvent("WeixinJSBridgeReady", jsApiCall);
                                document.attachEvent("onWeixinJSBridgeReady", jsApiCall);
                            }
                        }else{
                            jsApiCall();
                        }
                    }
                </script>
                <script type="text/javascript">
                    //获取共享地址
                    function editAddress()
                    {
                        WeixinJSBridge.invoke(
                            "editAddress",%s,
                            function(res){
                                var value1 = res.proviceFirstStageName;
                                var value2 = res.addressCitySecondStageName;
                                var value3 = res.addressCountiesThirdStageName;
                                var value4 = res.addressDetailInfo;
                                var tel = res.telNumber;
            
            //				alert(value1 + value2 + value3 + value4 + ":" + tel);
                            }
                        );
                    }
            
                    window.onload = function(){
                        if (typeof WeixinJSBridge == "undefined"){
                            if( document.addEventListener ){
                                document.addEventListener("WeixinJSBridgeReady", editAddress, false);
                            }else if (document.attachEvent){
                                document.attachEvent("WeixinJSBridgeReady", editAddress);
                                document.attachEvent("onWeixinJSBridgeReady", editAddress);
                            }
                        }else{
                            editAddress();
                        }
                    };
            
                </script>
            </head>
            </html>', $jsApiParameters,$trade_id, $editAddress);
        $this->display();
    }


}
