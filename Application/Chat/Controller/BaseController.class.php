<?php
namespace Chat\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');

class BaseController extends Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->user = D('user');
        $weObj = new \Wechat();
        $result = $weObj->getOauthAccessToken();
        $openId = $result['openid'];
        $access = $result['access_token'];

//        $openId='oAdCq01YzcVjLWljmeEBFcDEswEY';

        if ($openId) {
            session('openid', $openId);
            session('access', $access);
            define('OPEN_ID', session('openid'));

        }

        //立用户信息
        if (!$this->user->getUser()) {
            $weObj = new \Wechat();
            $userInfo = $weObj->getOauthUserinfo(session('access'), session('openid'));
            if ($userInfo) {
                $re = $this->user->addUser($userInfo);
                if (!$re)
                    $this->error('请您通过我们的微信公众号（筑影学堂）登陆哦', U('User/index'));
            }
        }
    }

    public function time_zhuanti($time)
    {
//        2017-11-12 01:30
        //判断上下午
        $h=substr($time,11,2);
        if(intval($h)<=12)
            return substr_replace($time, ' 上午 ', 10, 0); // 0插入而非替换
        else{
            return substr_replace($time, ' 下午 ', 10, 0); // 0插入而非替换
        }


    }
    public function time_compare_min($time)
    {
//        2017-11-12 01:30
        //判断上下午.
        $now = date('Y-m-d H:i:s');
        $s = strtotime($time);
        $min = round((strtotime($now)-$s)/60);
        return $min;


    }
    public function time_day($time)
    {
        return substr($time, 0, 11);

    }
}