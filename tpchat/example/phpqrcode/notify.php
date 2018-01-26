<?php

ini_set('date.timezone','Asia/Shanghai');
error_reporting(E_ERROR);
require_once "../lib/WxPay.Api.php";
require_once '../lib/WxPay.Notify.php';
require_once 'log.php';
header('conten-type:text/html;charset=utf-8');
//初始化日志
$logHandler= new CLogFileHandler("../logs/".date('Y-m-d').'.log');
$log = Log::Init($logHandler, 15);

class PayNotifyCallBack extends WxPayNotify
{
	//查询订单
	public function Queryorder($transaction_id)
	{
		$input = new WxPayOrderQuery();
		$input->SetTransaction_id($transaction_id);
		$result = WxPayApi::orderQuery($input);
		Log::DEBUG("query:" . json_encode($result));
		if(array_key_exists("return_code", $result)
			&& array_key_exists("result_code", $result)
			&& $result["return_code"] == "SUCCESS"
			&& $result["result_code"] == "SUCCESS")
		{
			return true;
		}
		return false;
	}

	//重写回调处理函数
	public function NotifyProcess($data, &$msg)
	{
		Log::DEBUG("call back:" . json_encode($data));
		$notfiyOutput = array();

		if(!array_key_exists("transaction_id", $data)){
			$msg = "输入参数不正确";
			return false;
		}
		//查询订单，判断订单真实性
		if(!$this->Queryorder($data["transaction_id"])){
			$msg = "订单查询失败";
			return false;
		}
		return true;
	}
}

Log::DEBUG("begin notify");
$notify = new PayNotifyCallBack();
$notify->Handle(false);

$postStr = $GLOBALS["HTTP_RAW_POST_DATA"];
logger($postStr);
$xml=simplexml_load_string($postStr);

$con=mysql_connect('localhost','root','HuiTeng168')or die("sdf");

mysql_select_db("tpchat", $con);
$openid=$xml->openid;
$trade_id=$xml->attach;
$transaction_id=$xml->transaction_id;
mysql_query("set names utf8");
mysql_query("UPDATE trade SET trade_state = '已支付',transaction_id='$transaction_id'
          WHERE openid = '$openid' AND trade_id = '$trade_id'");
mysql_close($con);

if (isset($_GET)){
    echo "success";
}



//日志记录
function logger($log_content)
{
    $log_filename = "log".date('l jS \of F Y H:i:s').".xml";

    file_put_contents($log_filename,$log_content."\r\n", FILE_APPEND);


////
//    file_put_contents($log_filename,$log_content."\r\n", FILE_APPEND);
//
//    update($log_filename);
//

}

