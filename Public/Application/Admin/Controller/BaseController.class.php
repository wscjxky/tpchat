<?php
namespace Admin\Controller;
use Think\Controller;
class BaseController extends Controller{
	function __construct()
    {
        parent::__construct();
        //实现访问权限控制器过滤功能(防止翻墙访问)
        //1.获得当前请求的controller和action
//		$nowac=CONTROLLER_NAME."-".ACTION_NAME;
        //2.获得当前用户对应的角色权限


        if (session('account')) {

            $account = session('account');
    }

//		$manager_info=D('Admin')->find($account);
//		$role_id=$manager_info['role'];
//		$role_info=D('Role')->find($role_id);
//		$auth_ac=$role_info['value'];
//
//		//---------------------------------------------------------------//
//		//禁止未登录系统用户访问后台
		if(empty($account)){
            $this->redirect('admin/login','请您登陆',1);
		}
//		//---------------------------------------------------------------//
//
//		//A.判断用户当前请求的controller和action是否在其权限列表中出现
//		//B.不要限制admin用户
//		//C.允许开放一些不加限制的权限
//		$allowac="Manager-login,Manager-verifyImg,Index-index,Index-head,Index-left,Index-right,Manager-logout";
//		$adminname=session('admin_user');
//		if(strpos($auth_ac, $nowac)===false && $adminname!=='admin' && strpos($allowac, $nowac)===false){
//			exit('没有权限访问');
//		}
//

	}
}