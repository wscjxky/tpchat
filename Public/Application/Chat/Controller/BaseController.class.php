<?php
namespace Chat\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');

class BaseController extends Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->user=D('user');

        $weObj = new \Wechat();
        $result = $weObj->getOauthAccessToken();
        $openId = $result['openid'];
        $access = $result['access_token'];
//        $openId='oAdCq01YzcVjLWljmeEBFcDEswEY';
        if($openId) {
            session('openid', $openId);
            session('access', $access);
            define('OPEN_ID', session('openid'));

        }
        
        //立用户信息
        if(!$this->user->getUser()) {
            $weObj = new \Wechat();
            $userInfo = $weObj->getOauthUserinfo(session('access'),session('openid'));
            if($userInfo) {
                $re = $this->user->addUser($userInfo);
                if (!$re)
                    $this->error('请您通过我们的微信公众号（筑影学堂）登陆哦', U('User/index'));
            }
        }
    }
}