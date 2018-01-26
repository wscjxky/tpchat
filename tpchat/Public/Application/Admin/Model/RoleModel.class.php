<?php
namespace Model;
use Think\Model;

//角色model模型类
class RoleModel extends Model{
	//给角色分配权限，数据的制作和存储
	function saveAuth($authid,$roleid){
		//根据$authid制作ids字符串
		$auth_ids=implode(',', $authid);
		//根据$auth_ids获得对应的控制器和操作方法
		$auth_info=D('Auth')->field('auth_c,auth_a')->select("$auth_ids");
		//拼装controller和action
		$s="";
		foreach ($auth_info as $v){
			if(!empty($v['auth_a']))
				$s.=$v['auth_c']."-".$v['auth_a'].",";
		}
		$s=rtrim($s,',');  //去除最右侧逗号
		$sql="update sw_role set role_auth_ids='$auth_ids',role_auth_ac='$s' where role_id='$roleid'";
		return $this->execute($sql);
	}
	
}