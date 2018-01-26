<?php
namespace Chat\Model;
use Think\Model;
vendor('Wechat.wechat', '' ,'.php');

class UserModel extends Model {
    public function __construct()
    {
        parent::__construct();


    }

    public function addUser($userInfo){
        $openId=$userInfo['openid'];
        if($openId) {
            session('openid', $openId);
            define('OPEN_ID', session('openid'));
            if ($userInfo['sex'] != '1')
                $userInfo['sex'] = '女';
            else
                $userInfo['sex'] = '男';
            $data = array('openid' => $openId, 'username' => $userInfo['nickname'], 'chatname' => $userInfo['nickname'], 'profile' => $userInfo['headimgurl'], 'province' =>
                $userInfo['province'], 'city' => $userInfo['city'], 'gender' => $userInfo['sex']);

            return $this->add($data);
        }
        else
            return false;
    }

    public function getUser(){
            return $this->where(array('openid'=>session('openid')))->find();
    }

    public function isLogin(){
            return session('?openid');
    }


    public function getLog(){
        if($this->isLogin()){
            $log=D('log');
            $condition['openid'] = array(array('eq',''),array('eq',session('openid')), 'or') ;
            return $log->where($condition)->select();
        }
        return false;
    }
    public function getTrade(){
            $trade=D('trade');
            $result=$trade->query("SELECT*
                            FROM  `trade`  a
                            
                            INNER JOIN `course` b
                            
                            ON  a.course_id=b.course_id
                          
                            WHERE  a.openid='".OPEN_ID."'");
            return $result;

    }

    public function getAdvice(){
        $result=D('advice')->where(array("openid"=>OPEN_ID))->select();
        return $result;
    }
    public function getVideo(){

        $result=D('video')->where(array("openid"=>OPEN_ID))->select();
        return $result;
    }

}