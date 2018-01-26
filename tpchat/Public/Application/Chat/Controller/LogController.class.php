<?php
namespace Chat\Controller;
use Think\Controller;
class LogController extends Controller {


    public function index(){
        $user=D('user');
//        $data=array('openid'=>session('openid'),'content'=>"系统测试数据");
//        $log->add($data);
        $data = $user->getLog();
        $this->assign('data',array_reverse($data));
        $this->display();
    }
}